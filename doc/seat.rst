SEAT
====
SEAT(Speech Event Action Transfer) is a simple dialog manager for robotic applications.
The interactive behavior of the system can be realized without complex programming.

SEAT has following features:
 1. Paraphrase matching function.
 2. Conversation management function based on state transition model.
 3. Adapter functions (supports OpenRTM , BSD socket, etc...).

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

