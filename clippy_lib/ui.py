from __future__ import print_function

from six.moves import zip_longest


CLIPPY = '''\
    XXXXX
   X     X
-----+  +----+
| .  |  | .  |
|    |  |    |
-----+  +----+
  X      X
  X  X   X
  X  X   X   +------
  X  X   X
  X  X   X
  X  X  X  X
  X   XX  X
   X      X
    XXXXXX'''

PREAMBLE = '''\
I see you've added some bugs!
Maybe you need to change these files as well?'''

def _pad_line(line, width):
    tmp = max(width - len(line), 0)
    return line + (' '*tmp)

# prepare clippy
CLIPPY_LINES = CLIPPY.split('\n')
CLIPPY_WIDTH = max([len(line) for line in CLIPPY_LINES])
CLIPPY_LINES = [_pad_line(line, CLIPPY_WIDTH) for line in CLIPPY_LINES]

TEXT_WIDTH = 50


def _make_dialog(msg_lines, text_width):
    msg_lines = ['| {} |'.format(_pad_line(line, text_width)) for line in msg_lines]
    horiz_border = '-'*len(msg_lines[0])
    msg_lines.insert(0, horiz_border)
    msg_lines.append(horiz_border)
    return msg_lines


def output(suggested_files):
    # make message
    text_width = max(TEXT_WIDTH, max([len(line) for line in suggested_files]))
    msg_lines = [_pad_line(line, text_width) for line in PREAMBLE.split('\n')]
    msg_lines = msg_lines + ['', ''] + suggested_files

    # make dialog
    dialog = _make_dialog(msg_lines, text_width)
    dialog = ['', ''] + dialog

    # join image and dialog
    if len(dialog) > len(CLIPPY_LINES):
        fillvalue = ' '*CLIPPY_WIDTH
    else:
        fillvalue = ''
    parts = zip_longest(CLIPPY_LINES, dialog, fillvalue=fillvalue)
    lines = ['{}{}'.format(i[0], i[1]) for i in parts]

    # print it!
    print('\n'.join(lines))

