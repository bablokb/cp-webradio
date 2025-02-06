Uing OpenIconic-Font
====================

This project uses icons from the [Open Iconic
Font](https://www.appstudio.dev/app/OpenIconic.html).


Download
--------

To create your own subset (or use a different size) download the
TTF-version from
<https://github.com/iconic/open-iconic/blob/master/font/fonts/open-iconic.ttf?raw=true>.


Convert
-------

After download, convert the TTF-font to the BDF-format. Use the
[OTF2BDF-tool](https://github.com/jirutka/otf2bdf) for this task:

    otf2bdf -o open-iconic-24.bdf -p 24 open-iconic.ttf

Extract
-------

The BDF-format is human readable and you can extract the relevant
characters without problems (given that you use a decent editor). The
file has a header, and then for every character a `STARTCHAR
... ENDCHAR` block. You have to extract the header, all characters and
the final `ENDFONT` line. The header has a `CHARS` field that should
contain the number of characters. The subset in this repo uses 13
characters:

    caret-left          e02e
    media-play          e093
    media-step-backward e097
    media-step-forward  e098
    musical-note        e0a1
    pin                 e0a8
    reload              e0b3
    star                e0c2
    sun                 e0c3
    tag                 e0c5
    volume-high         e0d5
    volume-low          e0d6
    volume-off          e0d7

In the second column above you can see the unicode codepoint for the
character in the font. From Python, you reference this character as
e.g.  `"\uE097"` (media-step-backward). See `src/logo.py` on how
the code uses these characters for the buttons.

A mapping of characters to unicode codepoints is available in the
[css-file](https://github.com/iconic/open-iconic/blob/master/font/css/open-iconic-foundation.css)
of the font.
