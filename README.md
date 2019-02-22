# 2019-02-touchfix
Works around some issues related to invalid touch event handling in some applications (often GTK based).
This script runs as root in the background and listens for touch events. In case of such event it fires 
the appropriate pointer events instead of touch events to get the broken applications working.

It also acts as a right click emulator.

In the long run this script will grab all events (don't let other listeners process them) and register itself as an input device on it's own.
It will then do gesture recognition emulate the appropriate pointer events (replaces software like touchegg).