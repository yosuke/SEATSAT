Usage: seatmltographviz [seatmlfile]

SEATスクリプトファイルからグラフを生成する

Options:
  --version      show program's version number and exit
  -h, --help     show this help message and exit
  -v, --verbose  デバッグ情報を表示する

Examples:

- SEATスクリプトファイルのグラフを生成する

  ::
  
  $ seatmltographviz sample.seatml | dot -Txlib

