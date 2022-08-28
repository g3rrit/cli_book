# CLI Book

Small CLI text file translation trainer.

This script can be used to read a text file on the command line and train translating every sentence
into a specific language.

The progress is saved to `~/.config/.cli_book.json`

## Usage

```
Usage: main.py [OPTIONS]

Options:
  --book TEXT   Name of the book  [required]
  --path TEXT   Path to the text file of the book
  --lang TEXT   Language of the book
  --nlang TEXT  Native language
  --help        Show this message and exit.
```

## Example

```
#################
DEN VERSTE BURSDAGEN.
-
:der schlechteste geburtstag
=
[0.94] ::: der schlimmste geburtstag aller zeiten.
```

