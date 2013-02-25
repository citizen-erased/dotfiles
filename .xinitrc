#!/bin/sh
#
# ~/.xinitrc
#
# Executed by startx (run your window manager from here)

if [ -d /etc/X11/xinit/xinitrc.d ]; then
  for f in /etc/X11/xinit/xinitrc.d/*; do
    [ -x "$f" ] && . "$f"
  done
  unset f
fi

# keyboard repeat rate + delay
xset r rate 170 50

# wallpaper
sh ~/.fehbg &

# run systemd as user instance
systemd --user &

# start window manager
exec i3

