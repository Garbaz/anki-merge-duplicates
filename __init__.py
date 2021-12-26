from anki.notes import Note
from aqt import mw
from aqt.utils import tooltip, qconnect
from aqt.qt import *
from aqt.browser import Browser
from aqt import gui_hooks


def merge_notes(note0: Note, note: Note) -> None:
    for f in note.keys():
        if f in note0 and note[f] > note0[f]:
            note0[f] = note[f]

    for t in note.tags:
        if not note0.hasTag(t):
            note0.addTag(t)

    note0.flush()


def merge_duplicates(browser: Browser) -> None:
    cardids = browser.selectedCards()
    cards = [mw.col.getCard(id) for id in cardids]
    notes = []

    for card in cards:
        note = card.note()
        if note.id not in [n.id for n in notes]:
            notes.append(note)

    dups: dict[list[Note]] = {}
    for note in notes:
        fields = note.items()
        dups.setdefault(fields[0], []).append(note)

    browser.model.beginReset()
    browser.mw.checkpoint("merge fields of duplicates")

    del_note_ids = []
    for dupl in dups.values():
        for i in range(1, len(dupl)):
            merge_notes(dupl[0], dupl[i])
            del_note_ids.append(dupl[i].id)

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
