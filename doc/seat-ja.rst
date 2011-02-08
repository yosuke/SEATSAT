SEAT0.rtc
=========
SEAT(Speech Event Action Transfer)はロボットアプリケーションのためのシンプルな対話マネージャです。
システムのインタラクティブな挙動を複雑なプログラミングなしで実現することができます。

SEATには以下の機能があります:
 1. パラフレーズマッチング機能
 2. 状態遷移モデルを用いた対話管理機能
 3. アダプタ機能(OpenRTM, BSD socketなどとの接続ができます).

:Vendor: Yosuke Matsusaka and Isao Hara, AIST
:Version: 1.03
:Category: Speech

Ports
-----
.. csv-table:: Ports
   :header: "Name", "Type", "DataType", "Description"
   :widths: 8, 8, 8, 26
   
   "speechin", "DataInPort", "TimedString", ""
   "speechout", "DataOutPort", "TimedString", ""

Configuration parameters
------------------------
.. csv-table:: Configration parameters
   :header: "Name", "Description"
   :widths: 12, 38
   
   "scriptfile", ""

