#!/usr/bin/python3
"""
Binary heat map generator

Visit <https://github.com/jwodder/binheat> for more information.
"""

__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'binheat@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/binheat'

import re
import click
from   reportlab.pdfbase         import pdfmetrics
from   reportlab.pdfbase.ttfonts import TTFont
from   reportlab.pdfgen.canvas   import Canvas

EM = 0.7  # expected em-to-font-size ratio
PADDING = 5
LABEL_PAD = 2.5

COL_BG_COLOR = (0.8, 0.8, 0.8)
ROW_BG_COLOR = (1, 1, 0.5)

class BinHeat:
    def __init__(self, allow_extra=False):
        #: Whether to allow (True) or discard (False) pairs containing an
        #: unknown label.  Only has an effect when
        #: `set_row_labels()`/`set_column_labels()` has been called.
        self.allow_extra = allow_extra
        self.row_labels_set = False
        self.column_labels_set = False
        self.rows2indices = {}
        self.columns2indices = {}
        self.pairs = set()

    def set_row_labels(self, labels):
        if self.row_labels_set:
            raise RuntimeError('set_row_labels() called more than once')
        elif self.pairs:
            raise RuntimeError('set_row_labels() called after add_pair()')
        else:
            self.row_labels_set = True
        self.rows2indices = {l:i for i,l in enumerate(labels)}

    def set_column_labels(self, labels):
        if self.column_labels_set:
            raise RuntimeError('set_column_labels() called more than once')
        elif self.pairs:
            raise RuntimeError('set_column_labels() called after add_pair()')
        else:
            self.column_labels_set = True
        self.columns2indices = {l:i for i,l in enumerate(labels)}

    def add_pair(self, row, column):
        if not self.allow_extra:
            if self.row_labels_set and row not in self.rows2indices:
                return
            if self.column_labels_set and column not in self.columns2indices:
                return
        if row not in self.rows2indices:
            self.rows2indices[row] = len(self.rows2indices)
        if column not in self.columns2indices:
            self.columns2indices[column] = len(self.columns2indices)
        self.pairs.add((row, column))

    @property
    def rows(self):
        """ The number of distinct row labels in the binary heat map """
        return len(self.rows2indices)

    @property
    def columns(self):
        """ The number of distinct column labels in the binary heat map """
        return len(self.columns2indices)

    @property
    def row_labels(self):
        return sorted(
            self.rows2indices.keys(),
            key=self.rows2indices.__getitem__,
        )

    @property
    def column_labels(self):
        return sorted(
            self.columns2indices.keys(),
            key=self.columns2indices.__getitem__,
        )

    def get_indexed_pairs(self):
        for r,c in self.pairs:
            yield (self.rows2indices[r], self.columns2indices[c])

    def sort_labels(self):
        ### TODO: Take allow_extra into account when *_labels_set
        if not self.row_labels_set:
            self.rows2indices = {
                k:i for i,k in enumerate(sorted(self.rows2indices.keys()))
            }
        if not self.column_labels_set:
            self.columns2indices = {
                k:i for i,k in enumerate(sorted(self.columns2indices.keys()))
            }

    def render(self, outfile, font_name, font_size):
        c = Canvas(outfile)
        c.setFont(font_name, font_size)
        leftlen = max(map(c.stringWidth, self.row_labels)) + LABEL_PAD * 2
        toplen  = max(map(c.stringWidth, self.column_labels)) + LABEL_PAD * 2
        miny = self.rows * font_size * 1.2
        maxx = self.columns * font_size * 1.2
        c.setPageSize((leftlen + maxx + PADDING*2, miny + toplen + PADDING*2))
        # Set coordinates so that LL corner has coord (-leftlen-PADDING,
        # -miny-PADDING) and the origin is at the point where the borders of the
        # row & column labels meet:
        c.translate(leftlen+PADDING, miny+PADDING)

        lineheight = font_size * 1.2
        radius = lineheight / 3

        c.setFillColorRGB(*COL_BG_COLOR)
        for i in range(0, self.columns, 2):
            c.rect(
                i * lineheight,
                -miny,
                lineheight,
                miny + toplen,
                stroke=0,
                fill=1,
            )

        c.setFillColorRGB(*ROW_BG_COLOR)
        for i in range(2, self.rows+1, 2):
            # Yes, it starts at 2, so that the positive rectangle height will
            # make it fill row 1.
            c.rect(
                -leftlen,
                -i * lineheight,
                leftlen + maxx,
                lineheight,
                stroke=0,
                fill=1,
            )

        c.setFillColorRGB(0, 0, 0)
        c.line(0, toplen, 0, -miny)
        c.line(-leftlen, 0, maxx, 0)

        for i, label in enumerate(self.row_labels):
            c.drawRightString(
                -LABEL_PAD,
                -(i+1) * lineheight + font_size / 3,
                label,
            )

        for i, label in enumerate(self.column_labels):
            c.saveState()
            c.translate((i+1) * lineheight, 0)
            c.rotate(90)
            c.drawString(LABEL_PAD, font_size / 3, label)
            c.restoreState()

        for row, col in self.get_indexed_pairs():
            c.circle(
                (col+0.5) * lineheight,
                -(row+0.5) * lineheight,
                radius,
                stroke=0,
                fill=1,
            )

        c.showPage()
        c.save()


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option('-F', '--font', metavar='TTF_FILE',
              help='Typeset text in given font')
@click.option('-f', '--font-size', type=float, default=12, show_default=True,
              help='Size of normal text')
@click.option('-T', '--transpose', is_flag=True)
@click.option('-m', '--multiline', is_flag=True)
@click.option('-S', '--no-sort', is_flag=True)
@click.option('-1', '--left-labels', type=click.File())
@click.option('-2', '--top-labels', type=click.File())
@click.argument('infile', type=click.File(), default='-')
@click.argument('outfile', type=click.File('wb'), default='-')
def main(infile, outfile, font, font_size, transpose, multiline, no_sort,
         left_labels, top_labels):
    if font is not None:
        font_name = 'CustomFont'
        ### TODO: Use the basename of the filename as the font name?  (Could
        ### that ever cause problems?)
        pdfmetrics.registerFont(TTFont(font_name, font))
    else:
        font_name = 'Times-Roman'

    bh = BinHeat()

    if transpose:
        left_labels, top_labels = top_labels, left_labels
    if left_labels:
        bh.set_row_labels(strip_read(left_labels))
    if top_labels:
        bh.set_column_labels(strip_read(top_labels))

    for line in strip_read(infile):
        left, *top = re.split(r'\t+', line)
        for t in (top if multiline else top[:1]):
            if transpose:
                bh.add_pair(t, left)
            else:
                bh.add_pair(left, t)

    if not no_sort:
        bh.sort_labels()

    bh.render(outfile, font_name, font_size)

def strip_read(fp):
    r"""
    Yield the lines in file ``fp`` with trailing whitespace stripped and with
    lines beginning with ``/^\s*#/`` (i.e., comment lines) discarded
    """
    for line in fp:
        line = line.rstrip()
        if line == '' or line.lstrip().startswith('#'):
            continue
        yield line

if __name__ == '__main__':
    main()
