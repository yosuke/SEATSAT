Usage: seatmltographviz [seatmlfile]

SEATスクリプトファイルからグラフを生成する

Options:
  --version      プログラムのバージョンを表示して終了する
  -h, --help     このヘルプ画面を表示して終了する
  -v, --verbose  デバッグ情報を表示する

Examples:

- SEATスクリプトファイルのグラフを生成する

  ::
  
  $ seatmltographviz sample.seatml | dot -Txlib

