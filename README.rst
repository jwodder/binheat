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
| `Changelog <https://github.com/jwodder/binheat/blob/master/CHANGELOG.md>`_

``binheat`` converts a description of a binary relation into a PDF image of the
relation as a binary heat map (a.k.a. matrix display, adjacency matrix,
comparison chart, and probably a bunch of other names as well; see below for an
example).

Each line of the input (except for blank lines and comments, which are ignored)
must be of the form ``x<TAB>y<TAB>z...``, denoting pairs ``(x, y)``, ``(x,
z)``, etc. in the binary relation.

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

Input is read from ``<infile>`` (defaulting to standard input), and the
resulting PDF is written to ``<outfile>`` (defaulting to ``<infile>`` with its
file extension changed to ``.pdf``, or to standard output if ``<infile>`` is
standard input).


Options
-------

- ``-C <file>``, ``--column-labels <file>`` — Use the lines in ``<file>``
  (after discarding blank lines & comments) in the order they appear as column
  labels (or row labels if ``--transpose`` is in effect).  Any pairs in the
  input whose second column does not appear in ``<file>`` are discarded.

- ``-F <font>``, ``--font <font>`` — Typeset text in the given font.
  ``<font>`` must be either the name of a builtin PostScript font or the path
  to a ``.ttf`` file.  By default, text is typeset in Times-Roman.

- ``-f <size>``, ``--font-size <size>`` — Set the text size to ``<size>``
  (default 12).

- ``-R <file>``, ``--row-labels <file>`` — Use the lines in ``<file>`` (after
  discarding blank lines & comments) in the order they appear as row labels (or
  column labels if ``--transpose`` is in effect).  Any pairs in the input whose
  first column does not appear in ``<file>`` are discarded.

- ``--sort/--no-sort`` — Whether to list labels in the output in lexical order
  rather than in the order in which they appear in the input file; default:
  ``--no-sort``

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

produces (using the default options) an output file that looks like this:

.. image:: https://github.com/jwodder/binheat/raw/v0.2.0/examples/ctype.png
