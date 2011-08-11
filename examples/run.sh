#!/bin/sh

echo "exiting existing components..."
rtexit /localhost/`hostname`.host_cxt/SEAT0.rtc
rtexit /localhost/`hostname`.host_cxt/ConsoleIn0.rtc
sleep 3

echo "launching components..."
gnome-terminal -x python ConsoleIn.py
gnome-terminal -x seat sample.seatml
sleep 3

echo "connecting components..."
rtcon /localhost/`hostname`.host_cxt/ConsoleIn0.rtc:out /localhost/`hostname`.host_cxt/SEAT0.rtc:speechin

echo "activating components..."
rtact /localhost/`hostname`.host_cxt/SEAT0.rtc
rtact /localhost/`hostname`.host_cxt/ConsoleIn0.rtc

echo "testing for 15 seconds..."
sleep 15

echo "exiting components..."
rtexit /localhost/`hostname`.host_cxt/SEAT0.rtc
rtexit /localhost/`hostname`.host_cxt/ConsoleIn0.rtc
