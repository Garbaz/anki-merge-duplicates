# Anki Merge Duplicates

A simple anki addon to merge duplicate notes into a single note.

## Installation

Install the addon from [AnkiWeb](https://ankiweb.net/shared/info/55394168) or manually my cloning this repo in `{Anki Directory}/addons21/`.

## Usage

Select any number of notes/cards in the browser, right-click, and press "Merge duplicate notes".

Of all the selected notes, any duplicates (i.e. the first field being equal) will be merged together. The merging strategy can be configured, see below. The tags of all notes are combined, i.e. the merged note will have all the tags any of the original notes had.

Say for example you select these notes:

Word | Description | Audio | tags
--|--|--|--
banana | a long yellow fruit growing in tropical climates | | very-important-tag
banana | a fruit | [sound:banana.mp3] | fruit, marked
apple | a round, red or green fruit | | fruit

and press "Merge duplicate notes".

The first two notes, their first field being equal, will be detected as duplicates of each other. So these two notes will be combined into one note, whereas the "apple" note will remain untouched.

When two notes that get merged have different values in one field, the default strategy is to pick the longer one. In the example for the "Description" field, the first note has the longer value, so the merged note will have it's "Description" value. For the "Audio" field however, the second note has the longer value (the field being empty for the first note), so the merged note will have it's "Audio" value.

The tags will be combined of the two notes.

So the result will be:

Word | Description | Audio | tags
--|--|--|--
banana | a long yellow fruit growing in tropical climates | [sound:banana.mp3] | very-important-tag, fruit, marked
apple | a round, red or green fruit | | fruit

## Config

Currently the configuration has only one option `merge_mode`, it can be set to the following values:
* `longer` (default) – The longer content of the notes will be kept for the merged note, see above.
* `concat` – The contents of both notes will be concatenated for the new note.
* `skip` – Notes will only get merged if there are no conflicting fields. Merges will only happen if for all fields both notes have the same value or one note has no value.

If you are comfortable with Python and want to change something, you should be able to just change the addon yourself, it's very small. Click "View files" in the addon menu in Anki to get to the folder, and open `__init__.py`.

_Note:_ If you have installed the addon from AnkiWeb, if I ever push an update of the addon there, any local changes will be overwritten when it gets updated. If you install the addon manually, this will not happen. 
