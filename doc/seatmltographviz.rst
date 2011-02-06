Usage: seatmltographviz [seatmlfile]

Draw graph from SEAT script file.

Options:
  --version      show program's version number and exit
  -h, --help     show this help message and exit
  -v, --verbose  output verbose information

Examples:

- Draw graph of the SEAT script file.

  ::
  
  $ seatmltographviz sample.seatml | dot -Txlib
