.. image:: http://www.repostatus.org/badges/latest/wip.svg
    :target: http://www.repostatus.org/#wip
    :alt: Project Status: WIP — Initial development is in progress, but there
          has not yet been a stable, usable release suitable for the public.

.. image:: https://img.shields.io/pypi/pyversions/binheat.svg
    :target: https://pypi.org/project/binheat/

.. image:: https://img.shields.io/github/license/jwodder/binheat.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
    :target: https://saythanks.io/to/jwodder

`GitHub <https://github.com/jwodder/binheat>`_
| `PyPI <https://pypi.org/project/binheat/>`_
| `Issues <https://github.com/jwodder/binheat/issues>`_

``binheat`` converts a description of a binary relation into a PDF image of the
relation as a binary heat map (a.k.a. matrix display, adjacency matrix,
comparison chart, and probably a bunch of other names as well).  The input must
list the elements of the relation, one per line, each line consisting of two
labels (nonempty nontab character sequences) separated by one or more tabs.
(The input may also contain comment lines in which the first nonwhitespace
character is ``#``.)  ``binheat`` will then render a PDF file showing a table
in which the labels from the first column of each line are lexically sorted
along the left edge, the labels from the second column are lexically sorted
along the top edge, and dots are placed in the cells of the table to represent
the elements of the relation.


Installation
============
``binheat`` requires Python 3.4 or higher.  Just use `pip
<https://pip.pypa.io>`_ for Python 3 (You have pip, right?) to install
``binheat`` and its dependencies::

    python3 -m pip install binheat


Usage
=====

::

    binheat [<OPTIONS>] [<infile> [<outfile>]]

Input is read from ``<infile>`` (or standard input if no file is specified),
and the resulting PDF is written to ``<outfile>`` (or standard output if no
file is specified).


Options
-------

- ``-C <file>``, ``--column-labels <file>`` — The lines of ``<file>`` will be
  taken as a list of all labels appearing in the second column of the input
  file, and the labels along the top edge of the output chart (or the left edge
  if ``--transpose`` is in effect) will be in the same order that they are
  listed in ``<file>``.  Labels that appear in ``<file>`` but not the second
  column of the input file will appear in the output with no relations, and
  labels that appear in the second column of the input file but not ``<file>``
  will not appear in the output at all.

  This option overrides the ``--no-sort`` option for the second column only.

- ``-F <ttf-file>``, ``--font <ttf-file>`` — Use the given ``.ttf`` file for
  the text font.  By default, all text is typeset in Times-Roman.

- ``-f <size>``, ``--font-size <size>`` — Set the text size to ``<size>``
  (default 12).

- ``-m``, ``--multiline`` — ``foo<TAB>bar<TAB>baz`` (or any number of
  tab-separated fields) will be allowed as an abbreviation for ``foo<TAB>bar``
  followed by ``foo<TAB>baz`` etc.

- ``-R <file>``, ``--row-labels <file>`` — The lines of ``<file>`` will be
  taken as a list of all labels appearing in the first column of the input
  file, and the labels along the left edge of the output chart (or the top edge
  if ``--transpose`` is in effect) will be in the same order that they are
  listed in ``<file>``.  Labels that appear in ``<file>`` but not the first
  column of the input file will appear in the output with no relations, and
  labels that appear in the first column of the input file but not ``<file>``
  will not appear in the output at all.

  This option overrides the ``--no-sort`` option for the first column only.

- ``-S``, ``--no-sort`` — Labels in the output will be listed in the order in
  which they appear in the input file rather than in lexical order

- ``-T``, ``--transpose`` — The output will be transposed — i.e., the first
  column will be used for the top edge of the chart and the second column for
  the left edge.


Example
=======

The following input file::

    NUL (\0, 0x00)<TAB>iscntrl
    0x01..0x06<TAB>iscntrl
    BEL (\a, 0x07)<TAB>iscntrl
    BS (\b, 0x08)<TAB>iscntrl
    TAB (\t, 0x09)<TAB>iscntrl<TAB>isspace<TAB>isblank
    LF (\n, 0x0A)<TAB>iscntrl<TAB>isspace
    VT (\v, 0x0B)<TAB>iscntrl<TAB>isspace
    FF (\f, 0x0C)<TAB>iscntrl<TAB>isspace
    CR (\r, 0x0D)<TAB>iscntrl<TAB>isspace
    0x0E..0x1F<TAB>iscntrl
    SPACE (0x20)<TAB>isprint<TAB>isspace<TAB>isblank
    !"#$%&'()*+,-./<TAB>isprint<TAB>isgraph<TAB>ispunct
    0123456789<TAB>isprint<TAB>isgraph<TAB>isalnum<TAB>isdigit<TAB>isxdigit
    :;<=>?@<TAB>isprint<TAB>isgraph<TAB>ispunct
    ABCDEF<TAB>isprint<TAB>isgraph<TAB>isalnum<TAB>isalpha<TAB>isupper<TAB>isxdigit
    GHIJKLMNOPQRSTUVWXYZ<TAB>isprint<TAB>isgraph<TAB>isalnum<TAB>isalpha<TAB>isupper
    [\]^_`<TAB>isprint<TAB>isgraph<TAB>ispunct
    abcdef<TAB>isprint<TAB>isgraph<TAB>isalnum<TAB>isalpha<TAB>islower<TAB>isxdigit
    ghijklmnopqrstuvwxyz<TAB>isprint<TAB>isgraph<TAB>isalnum<TAB>isalpha<TAB>islower
    {|}~<TAB>isprint<TAB>isgraph<TAB>ispunct
    DEL (0x7F)<TAB>iscntrl

produces (using the ``--multiline`` and ``--no-sort`` options) an output file
that looks like this:

.. image:: https://github.com/jwodder/binheat/raw/master/examples/ctype.png
