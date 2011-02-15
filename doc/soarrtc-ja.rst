SoarRTC
=======
プロダクションシステムエンジンSoarを用いた汎用人工知能コンポーネント

:Vendor: AIST
:Version: 1.03
:Category: communication

Ports
-----
.. csv-table:: Ports
   :header: "Name", "Type", "DataType", "Description"
   :widths: 8, 8, 8, 26
   
   "inport0", "DataInPort", "TimedString, Any", ""
   "outport0", "DataOutPort", "TimedString, Any", ""
   "command", "DataOutPort", "TimedString", ""

.. digraph:: comp

   rankdir=LR;
   SoarRTC [shape=Mrecord, label="SoarRTC"];
   inport0 [shape=plaintext, label="inport0"];
   inport0 -> SoarRTC;
   outport0 [shape=plaintext, label="outport0"];
   SoarRTC -> outport0;
   command [shape=plaintext, label="command"];
   SoarRTC -> command;

