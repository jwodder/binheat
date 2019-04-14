#!/usr/bin/python3
from   collections               import defaultdict
import re
import click
from   reportlab.pdfbase         import pdfmetrics
from   reportlab.pdfbase.ttfonts import TTFont
from   reportlab.pdfgen.canvas   import Canvas

EM = 0.7  # expected em-to-font-size ratio
PADDING = 5
LINEPAD = 2.5

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

    matrix = defaultdict(dict)

    def pushPair(left, top):
        nonlocal rows, cols
        if transpose:
            left, top = top, left
        matrix[left][top] = 1
        if no_sort and not left_labels and left not in lefts:
            lefts[left] = rows
            rows += 1
        if no_sort and not top_labels and top not in tops:
            tops[top] = cols
            cols += 1

    if transpose:
        left_labels, top_labels = top_labels, left_labels

    lefts = readList(left_labels) if left_labels else {}
    rows = len(lefts)

    tops = readList(top_labels) if top_labels else {}
    cols = len(tops)

    for line in infile:
        line = line.rstrip()
        if line == '' or line.lstrip().startswith('#'):
            continue
        left, *top = re.split(r'\t+', line)
        if multiline:
            for t in top:
                pushPair(left, t)
        elif top:
            pushPair(left, top[0])

    if not no_sort:
        if not left_labels:
            lefts = {k:i for i,k in enumerate(sorted(matrix.keys()))}
            rows = len(lefts)
        if not top_labels:
            tops_set = set()
            for v in matrix.values():
                tops_set.update(v.keys())
            tops = {k:i for i,k in enumerate(sorted(tops_set))}
            cols = len(tops)

    ### TODO: Use canvas.stringWidth() here instead:
    leftlen = max(map(len, lefts.keys())) * EM * font_size
    toplen  = max(map(len, tops.keys()))  * EM * font_size

    miny = rows * font_size * 1.2
    maxx = cols * font_size * 1.2

    c = Canvas(
        outfile,
        (leftlen + maxx + PADDING * 2, miny + toplen + PADDING * 2),
    )
    # Set coordinates so that LL corner has coord (-leftlen-PADDING,
    # -miny-PADDING):
    c.translate(leftlen+PADDING, miny+PADDING)

    c.setFont(font_name, font_size)

    lineheight = font_size * 1.2
    radius = lineheight / 3

    def dot(canvas, col, row):
        canvas.circle(
            (col+0.5) * lineheight,
            -(row+0.5) * lineheight,
            radius,
            stroke=0,
            fill=1,
        )

    c.setFillColorRGB(0.8, 0.8, 0.8)
    for i in range(0, cols, 2):
        c.rect(
            i * lineheight,
            -miny,
            lineheight,
            miny + toplen,
            stroke=0,
            fill=1,
        )

    c.setFillColorRGB(1, 1, 0.5)
    for i in range(2, rows+1, 2):
        # Yes, it starts at 2, so that the positive rectangle height will make
        # it fill row 1.
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

    for k,v in lefts.items():
        ### TODO: Replace with drawRightString()?
        c.drawString(
            -c.stringWidth(k) - LINEPAD,
            -(v+1) * lineheight + font_size / 3,
            k,
        )

    for k,v in tops.items():
        c.saveState()
        c.translate((v+1) * lineheight, 0)
        c.rotate(90)
        c.drawString(LINEPAD, font_size / 3, k)
        c.restoreState()

    for k,v in matrix.items():
        if k in lefts:
            for j in v.keys():
                if j in tops:
                    dot(c, tops[j], lefts[k])

    c.showPage()
    c.save()

def readList(fp):
    i = 0
    lines2nums = {}
    for line in fp:
        line = line.rstrip()
        if line == '' or line.lstrip().startswith('#'):
            continue
        lines2nums[line] = i
        i += 1
    return lines2nums

if __name__ == '__main__':
    main()
