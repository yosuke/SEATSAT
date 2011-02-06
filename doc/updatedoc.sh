#!/bin/sh

rtexit /localhost/`hostname`.host_cxt/SEAT0.rtc
seat ../examples/sample.seatml&
sleep 2
rtdoc --format=rst /localhost/`hostname`.host_cxt/SEAT0.rtc > seat.rst
rtexit /localhost/`hostname`.host_cxt/SEAT0.rtc

rtexit /localhost/`hostname`.host_cxt/SoarRTC0.rtc
soarrtc &
sleep 2
rtdoc --format=rst /localhost/`hostname`.host_cxt/SoarRTC0.rtc > soarrtc.rst
rtexit /localhost/`hostname`.host_cxt/SoarRTC0.rtc

validateseatml --help > validateseatml.rst

seatmltosrgs --help > seatmltosrgs.rst

seatmltographviz --help > seatmltographviz.rst

