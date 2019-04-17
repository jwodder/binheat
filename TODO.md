- Add an option for appending values found in the input but not in the -R/-C
  files to the output
    - When sorting with this option on, the resulting sequence of labels should
      be the labels in -R/-C in the same order followed by the extra labels
      sorted
- Improve handling of empty fields
    - Currently, `binheat.py` will ignore a line of the form "`label<TAB><EOL>`"
      but will treat a line of the form "`<TAB>label<EOL>`" as denoting a
      relationship from an empty label to "`label`".  Either eliminate the
      latter behavior or treat lines with a single label as just establishing
      that the label exists (meaningful only when `-S` is in effect).
- Add an option for emitting a warning when a field not in a supplied -R/-C
  file is encountered
- Support comments at the ends of nonempty lines?
- Add more example input files
- Should the `-m` option always be in effect?
- Make `--no-sort` the default behavior and add a `--sort` option
- Make the margins configurable on the command line?
- Implement the drawing logic as a `reportlab.*.Flowable` subclass (or factory
  thereof?)
- `--multiline` is the wrong name for the option.  Rename it.
- Rethink how `--transpose` interacts with `-R` and `-C`
