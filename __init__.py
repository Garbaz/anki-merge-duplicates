from anki.notes import Note
from aqt import gui_hooks, mw
from aqt.browser import Browser
from aqt.qt import *
from aqt.utils import qconnect, showCritical, tooltip

config = mw.addonManager.getConfig(__name__)


def merge_notes(note0: Note, note: Note, mode: str) -> None:
    for f in note.keys():
        if f in note0 and note0[f] != note[f]:
            if mode == "concat":
                note0[f] += note[f]
            elif mode == "longer" and len(note[f]) > len(note0[f]):
                note0[f] = note[f]
            elif mode == "skip":
                raise ValueError("Conflicting entries")
            else:
                raise NotImplementedError("Unknown mode %s" % mode)

    for t in note.tags:
        if not note0.hasTag(t):
            note0.addTag(t)

    note0.flush()


def merge_duplicates(browser: Browser) -> None:
    mode = config.get("merge_mode", "longer")
    cardids = browser.selectedCards()
    cards = [mw.col.getCard(id) for id in cardids]
    notes = []

    for card in cards:
        note = card.note()
        if note.id not in [n.id for n, _ in notes]:
            notes.append((note, card.reps))

    dups: dict[list[Note]] = {}
    for note, reps in notes:
        fields = note.items()
        dups.setdefault(fields[0], []).append((note, reps))

    browser.model.beginReset()
    browser.mw.checkpoint("merge fields of duplicates")

    del_note_ids = []
    for dupl in dups.values():
        dupl = [note for note, reps in sorted(dupl, key=lambda x: -x[1])]
        for i in range(1, len(dupl)):
            try:
                merge_notes(dupl[0], dupl[i], mode)
                del_note_ids.append(dupl[i].id)
            except ValueError:
                pass
            except NotImplementedError:
                showCritical("Invalid configuration", parent=browser)
                return

    browser.mw.col.remNotes(del_note_ids)

    browser.model.endReset()
    browser.mw.reset()

    tooltip(f"Successfully merged {len(del_note_ids)} notes.", parent=browser)


def setup_context_menu(browser: Browser):
    menu = browser.form.menu_Cards
    merge_action = menu.addAction("Merge duplicate notes")
    qconnect(merge_action.triggered, browser.onMergeDuplicates)


Browser.onMergeDuplicates = merge_duplicates
gui_hooks.browser_menus_did_init.append(setup_context_menu)
