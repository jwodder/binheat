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
- Make the margins configurable on the command line?
- Implement the drawing logic as a `reportlab.*.Flowable` subclass (or factory
  thereof?)
- Rethink how `--transpose` interacts with `-R` and `-C`
- Add an option for making the column headers slanted (Do it by default?)
- Come up with a new unified input format that allows one to specify everything
  about the chart's contents in a single file
    - Include a means to specify the locations of horizontal & vertical rules
      between rows/columns
    - Include a means to specify various different symbols at "hot points"
- Add a function that takes loaded input data, renders a chart, and returns a
  `Canvas` object?  Saves a `Canvas` object to a given path?
- Add a `Binheat` class for containing just the row names, column names, and
  relation members
    - Give it a classmethod for constructing from an input file and test it
    - Give it a method for rendering as a PDF or some other reportlab object
