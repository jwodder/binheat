- Add an option for appending values found in the input but not in the -1/-2
  files to the output
    - When sorting with this option on, the resulting sequence of labels should
      be the labels in -1/-2 in the same order followed by the extra labels
      sorted
- Improve handling of empty fields
    - Currently, `binheat.py` will ignore a line of the form "`label<TAB><EOL>`"
      but will treat a line of the form "`<TAB>label<EOL>`" as denoting a
      relationship from an empty label to "`label`".  Either eliminate the
      latter behavior or treat lines with a single label as just establishing
      that the label exists (meaningful only when `-S` is in effect).
- Add an option for emitting a warning when a field not in a supplied -1/-2
  file is encountered
- Support comments at the ends of nonempty lines?
- Add more example input files
- Should the `-m` option always be in effect?
- Make `--no-sort` the default behavior and add a `--sort` option
- Convert `binheat.pod` to a `README.rst`
    - Add a link to the repository to the documentation
    - Rewrite RESTRICTIONS section to address some characters not being
      available in selected fonts
- Support specifying builtin fonts with `--font` (The available builtin fonts
  can be listed with `Canvas(*).getAvailableFonts()`)
- Make the margins configurable on the command line?
- When an input filename is given but no output filename, write to the input
  filename with the extension set to `.pdf` instead of to stdout
- Implement the drawing logic as a `reportlab.*.Flowable` subclass (or factory
  thereof?)
- Add docstrings
- Add `--help` output
- Release on PyPI
