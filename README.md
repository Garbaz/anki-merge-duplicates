# Anki Merge Duplicates

A simple anki addon to merge duplicate notes into a single note.

## Installation

Install the addon from [AnkiWeb](https://ankiweb.net/shared/info/55394168) or manually my cloning this repo in `{Anki Directory}/addons21/`.

## Usage

Select any number of notes/cards in the browser, right-click, and press "Merge duplicate notes".

Of all the selected notes, any duplicates (i.e. the first field being equal) will be merged together, always taking the longer value of each field. The tags of all notes are combined, i.e. the merged note will have all the tags any of the original notes had.

Importantly, this will _not_ merge all selected notes.

Say for example you select these notes:

Word | Description | Audio | tags
--|--|--|--
banana | a long yellow fruit growing in tropical climates | | very-important-tag
banana | a fruit | [sound:banana.mp3] | fruit, marked
apple | a round, red or green fruit | | fruit

and press "Merge duplicate notes".

The first two notes, their first field being equal, will be detected as duplicates of each other. So these two notes will be combined into one note, whereas the "apple" note will remain untouched.

For the "Description" field, the first note has the bigger value, so the merged note will have it's "Description" value. For the "Audio" field however, the second note has the bigger value (the field being empty for the first note), so the merged note will have it's "Audio" value.

The tags will be combined of the two notes.

So the result will be:

Word | Description | Audio | tags
--|--|--|--
banana | a long yellow fruit growing in tropical climates | [sound:banana.mp3] | very-important-tag, fruit, marked
apple | a round, red or green fruit | | fruit

## Config

Currently the addon has no configuration.

Though if you are comfortable with Python and want to change something, you should be able to just change the addon yourself, it's very small. Click "View files" in the addon menu in Anki to get to the folder, and open `__init__.py`.

_Note:_ If you have installed the addon from AnkiWeb, whenever I push an update of the addon there, any local changes will be overwritten. If you install the addon manually, this will not happen. 