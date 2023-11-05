#!/bin/sh

#Configurar segundo monitor a la derecha
mons -e right

#Picon config for all displays
DISPLAY=":0" picom -b & 

#----Icons system----

# systray battery icon
#cbatticon -u 5 &

#usb list
udiskie -t &

#network manager script
nm-applet &

# systray volume
# volumeicon &

#------------------

#Wallpaper charge
nitrogen --restore &

#configuracion teclado espaniol latino
#setxkbmap la-latin1'

# suspend after 15 minutes of inactivity
xidlehook --not-when-audio --not-when-fullscreen --timer 900 'systemctl suspend-then-hibernate' '' & # automatically suspend after 15 minutes of inactivity
