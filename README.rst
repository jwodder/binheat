.. image:: http://www.repostatus.org/badges/latest/active.svg
    :target: http://www.repostatus.org/#active
    :alt: Project Status: Active — The project has reached a stable, usable
          state and is being actively developed.

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
comparison chart, and probably a bunch of other names as well; see below for an
example).

Each line of the input (except for blank lines and comments, which are ignored)
must be of the form ``x<TAB>y``, denoting a pair ``(x, y)`` in the binary
relation.  If the ``--multiline`` option is given, an input line may instead
contain multiple tab-separated fields; ``x<TAB>a<TAB>b<TAB>c`` is then short
for ``x<TAB>a``, ``x<TAB>b``, and ``x<TAB>c``.

In the output table, the values from the first column of each input line become
the labels of the table's rows, and the values from the second input column
onwards become the labels of the table's columns.  This can be reversed with
the ``--transpose`` option.


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

- ``-C <file>``, ``--column-labels <file>`` — Use the lines in ``<file>``
  (after discarding blank lines & comments) in the order they appear as column
  labels (or row labels if ``--transpose`` is in effect).  Any pairs in the
  input whose second column does not appear in ``<file>`` are discarded.

- ``-F <ttf-file>``, ``--font <ttf-file>`` — Use the given ``.ttf`` file for
  the text font.  By default, all text is typeset in Times-Roman.

- ``-f <size>``, ``--font-size <size>`` — Set the text size to ``<size>``
  (default 12).

- ``-m``, ``--multiline`` — ``foo<TAB>bar<TAB>baz`` (or any number of
  tab-separated fields) will be allowed as an abbreviation for ``foo<TAB>bar``
  followed by ``foo<TAB>baz`` etc.

- ``-R <file>``, ``--row-labels <file>`` — Use the lines in ``<file>`` (after
  discarding blank lines & comments) in the order they appear as row labels (or
  column labels if ``--transpose`` is in effect).  Any pairs in the input whose
  first column does not appear in ``<file>`` are discarded.

- ``-S``, ``--no-sort`` — Labels in the output will be listed in the order in
  which they appear in the input file rather than in lexical order

- ``-T``, ``--transpose`` — The output will be transposed — i.e., the first
  column of the input will be used for the output table's column labels, and
  the second input column onwards will be used for the table's row labels.


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

.. image:: https://github.com/jwodder/binheat/raw/v0.1.0/examples/ctype.png
