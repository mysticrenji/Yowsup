#!/bin/bash
 
temp=$(/opt/vc/bin/vcgencmd measure_temp | cut -c6-7)
 
if [ "$temp" -gt 40 ]; then
   echo Whoa! My temperature is up to $(/opt/vc/bin/vcgencmd measure_temp). Power me down for a bit! | sendxmpp -t mysticrenji@jabber.hot-chilli.net
fi  
