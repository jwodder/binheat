#!/usr/bin/python3
"""
Binary heat map generator

``binheat`` converts a description of a binary relation into a PDF image of the
relation as a binary heat map (a.k.a. matrix display, adjacency matrix,
comparison chart, and probably a bunch of other names as well).

Each line of the input (except for blank lines and comments, which are ignored)
must be of the form ``x<TAB>y<TAB>z...``, denoting pairs ``(x, y)``, ``(x,
z)``, etc. in the binary relation.

In the output table, the values from the first column of each input line become
the labels of the table's rows, and the values from the second input column
onwards become the labels of the table's columns.  This can be reversed with
the ``--transpose`` option.

Run ``binheat --help`` or visit <https://github.com/jwodder/binheat> for more
information.
"""

__version__      = '0.2.0'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'binheat@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/binheat'

from   pathlib                   import Path
import re
import sys
import click
from   reportlab.pdfbase         import pdfmetrics
from   reportlab.pdfbase.ttfonts import TTFont
from   reportlab.pdfgen.canvas   import Canvas

#: Padding (in points) around the edge of the rendered binary heat map
PADDING = 5

#: Padding (in points) at the beginning & ending of the row & column labels
LABEL_PAD = 2.5

#: Color to use to highlight alternating columns
COL_BG_COLOR = (0.8, 0.8, 0.8)  # grey

#: Color to use to highlight alternating rows
ROW_BG_COLOR = (1, 1, 0.5)  # light yellow

class BinHeat:
    def __init__(self, allow_extra=False):
        #: Whether to allow (True) or discard (False) pairs containing an
        #: unknown label.  Only has an effect when
        #: `set_row_labels()`/`set_column_labels()` has been called.
        self.allow_extra = allow_extra
        #: Whether `set_row_labels()` has been called
        self.row_labels_set = False
        #: Whether `set_column_labels()` has been called
        self.column_labels_set = False
        #: Mapping from row labels to their indices when listed
        self.rows2indices = {}
        #: Mapping from column labels to their indices when listed
        self.columns2indices = {}
        #: Set of ``(row label, column label)`` pairs
        self.pairs = set()

    def set_row_labels(self, labels):
        """
        Set the row labels to the given sequence of strings in the order given

        :param labels: an iterable of strings to set the row labels to
        :raises RuntimeError: if called more than once or after calling
            `add_pair()`
        """
        if self.row_labels_set:
            raise RuntimeError('set_row_labels() called more than once')
        elif self.pairs:
            raise RuntimeError('set_row_labels() called after add_pair()')
        else:
            self.row_labels_set = True
        self.rows2indices = {l:i for i,l in enumerate(labels)}

    def set_column_labels(self, labels):
        """
        Set the column labels to the given sequence of strings in the order
        given

        :param labels: an iterable of strings to set the column labels to
        :raises RuntimeError: if called more than once or after calling
            `add_pair()`
        """
        if self.column_labels_set:
            raise RuntimeError('set_column_labels() called more than once')
        elif self.pairs:
            raise RuntimeError('set_column_labels() called after add_pair()')
        else:
            self.column_labels_set = True
        self.columns2indices = {l:i for i,l in enumerate(labels)}

    def add_pair(self, row, column):
        """
        Register a pairing of the given row and column.  If `allow_extra` is
        false and either component does not appear in a prespecified label set,
        the pair is discarded.  If `allow_extra` is true, new row or column
        labels are appended to the list of all row/column labels.

        :param str row: the label of the row of this point
        :param str column: the label of the column of this point
        """
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
        """ A list of all row labels in the binary heat map in display order """
        return sorted(
            self.rows2indices.keys(),
            key=self.rows2indices.__getitem__,
        )

    @property
    def column_labels(self):
        """
        A list of all column labels in the binary heat map in display order
        """
        return sorted(
            self.columns2indices.keys(),
            key=self.columns2indices.__getitem__,
        )

    def get_indexed_pairs(self):
        """
        Yield all pairs in the binary heat map in unspecified order, with each
        pair represented as a pairing of its row's index and its column's index
        """
        for r,c in self.pairs:
            yield (self.rows2indices[r], self.columns2indices[c])

    def sort_labels(self):
        """
        If `set_row_labels()` has not been called, reorder (and reindex) the
        row labels to be in lexicographic order.  Likewise for
        `set_column_labels()` and the column labels.
        """
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
        """
        Render the binary heat map as a PDF to the file-like object or filename
        ``outfile``.  All text will be typeset in the font named ``font_name``
        at size ``font_size``.
        """
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
@click.option('-C', '--column-labels', type=click.File(),
              help='Use lines in given file as column labels')
@click.option('-F', '--font', default='Times-Roman', show_default=True,
              help='Typeset text in given font', metavar='NAME|TTF_FILE')
@click.option('-f', '--font-size', type=float, default=12, show_default=True,
              help='Typeset text at given size')
@click.option('-R', '--row-labels', type=click.File(),
              help='Use lines in given file as row labels')
@click.option('--sort/--no-sort', '-s/-S', 'to_sort', is_flag=True,
              help='Sort the row & column labels')
@click.option('-T', '--transpose', is_flag=True,
              help='Exchange rows with columns')
@click.version_option(__version__, '-V', '--version',
                      message='binheat %(version)s')
@click.argument('infile', type=click.File(), default='-')
@click.argument('outfile', type=click.File('wb'), required=False)
def main(infile, outfile, font, font_size, transpose, to_sort, row_labels,
         column_labels):
    """
    Binary heat map generator

    ``binheat`` converts a description of a binary relation into a PDF image of
    the relation as a binary heat map (a.k.a. matrix display, adjacency matrix,
    comparison chart, and probably a bunch of other names as well).

    Each line of the input (except for blank lines and comments, which are
    ignored) must be of the form ``x<TAB>y<TAB>z...``, denoting pairs ``(x,
    y)``, ``(x, z)``, etc. in the binary relation.

    In the output table, the values from the first column of each input line
    become the labels of the table's rows, and the values from the second input
    column onwards become the labels of the table's columns.  This can be
    reversed with the ``--transpose`` option.

    Visit <https://github.com/jwodder/binheat> for more information.
    """
    if font in available_fonts():
        font_name = font
    else:
        # Assume we've been given a path to a .ttf file
        font_name = 'CustomFont'
        ### TODO: Use the basename of the filename as the font name?  (Could
        ### that ever cause problems?)
        pdfmetrics.registerFont(TTFont(font_name, font))

    bh = BinHeat()

    if transpose:
        row_labels, column_labels = column_labels, row_labels
    if row_labels:
        bh.set_row_labels(strip_read(row_labels))
    if column_labels:
        bh.set_column_labels(strip_read(column_labels))

    for line in strip_read(infile):
        left, *top = re.split(r'\t+', line)
        for t in top:
            if transpose:
                bh.add_pair(t, left)
            else:
                bh.add_pair(left, t)

    if to_sort:
        bh.sort_labels()

    if outfile is None:
        if infile is sys.stdin:
            outfile_name = '-'
        else:
            outfile_name = str(Path(infile.name).with_suffix('.pdf'))
        outfile = click.open_file(outfile_name, 'wb')

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

def available_fonts():
    return Canvas('').getAvailableFonts()
    #return pdfmetrics.standardFonts

if __name__ == '__main__':
    main()
