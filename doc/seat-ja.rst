SEAT
====
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

.. digraph:: comp

   rankdir=LR;
   SEAT [shape=Mrecord, label="SEAT"];
   speechin [shape=plaintext, label="speechin"];
   speechin -> SEAT;
   speechout [shape=plaintext, label="speechout"];
   SEAT -> speechout;

Configuration parameters
------------------------
.. csv-table:: Configuration parameters
   :header: "Name", "Description"
   :widths: 12, 38
   
   "scriptfile", ""

