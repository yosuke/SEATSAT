#!/bin/sh

rtexit /localhost/`hostname`.host_cxt/SEAT0.rtc
LANG=C seat ../examples/sample.seatml &
sleep 2
rtdoc --format=rst /localhost/`hostname`.host_cxt/SEAT0.rtc > seat.rst
rtexit /localhost/`hostname`.host_cxt/SEAT0.rtc
sleep 1
LANG=ja_JP.UTF-8 seat ../examples/sample.seatml &
sleep 2
rtdoc --format=rst /localhost/`hostname`.host_cxt/SEAT0.rtc > seat-ja.rst
rtexit /localhost/`hostname`.host_cxt/SEAT0.rtc

rtexit /localhost/`hostname`.host_cxt/SoarRTC0.rtc
LANG=C soarrtc &
sleep 2
rtdoc --format=rst /localhost/`hostname`.host_cxt/SoarRTC0.rtc > soarrtc.rst
rtexit /localhost/`hostname`.host_cxt/SoarRTC0.rtc
sleep 1
LANG=ja_JP.UTF-8 soarrtc &
sleep 2
rtdoc --format=rst /localhost/`hostname`.host_cxt/SoarRTC0.rtc > soarrtc-ja.rst
rtexit /localhost/`hostname`.host_cxt/SoarRTC0.rtc

LANG=C validateseatml --help > validateseatml.rst
LANG=ja_JP.UTF-8 validateseatml --help > validateseatml-ja.rst

LANG=C seatmltosrgs --help > seatmltosrgs.rst
LANG=ja_JP.UTF-8 seatmltosrgs --help > seatmltosrgs-ja.rst

LANG=C seatmltographviz --help > seatmltographviz.rst
LANG=ja_JP.UTF-8 seatmltographviz --help > seatmltographviz-ja.rst

