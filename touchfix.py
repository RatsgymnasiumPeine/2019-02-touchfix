##!/usr/bin/python3

import subprocess, time
import evdev
from evdev import AbsInfo, ecodes as e
from Xlib import X
from Xlib.display import Display
from Xlib.ext.xtest import fake_input
import time

TOUCH_PANEL_NAME = "Melfas LGD AIT Touch Controller" # This is my tablet's touch panel according to xinput. Edit it.
VALID_WINDOW_TYPES = ["_NET_WM_WINDOW_TYPE_POPUP_MENU"]
TOUCH_EVENT_CODE = 330
display = Display()
screen = display.screen()
left_click_button = 1
right_click_button = 3
upto_ten_fingers_touch_time = [None, None, None, None, None, None, None, None, None, None]

FIX_APPS = ["xfce4-panel"]

fixflag = False

between = 0
time_a = 0
time_b = 0

pos_a = None
pos_b = None


devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]

def common_member(a, b): 
    a_set = set(a) 
    b_set = set(b) 
    if (a_set & b_set): 
        return True 
    else: 
        return False


def getWindowTitles(window):
    try:
        children = window.query_tree().children
        child = []
        for w in children:
            n = w.get_wm_class()
            if n:
                child.append(n[0])
            
            child += getWindowTitles(w)
        return child
    except:
        return []

for device in devices:
    if (device.name == TOUCH_PANEL_NAME):
        input_node = device.path

device = evdev.InputDevice(input_node)
#device.grab()

for event in device.read_loop():
    try:
        if not event.code == TOUCH_EVENT_CODE:
            continue 
        
        print(evdev.util.categorize(event))     
        
        touch_window_type, touch_pos = None, None
        window = screen.root
        window_details = window.query_pointer()
        touch_pos = window_details._data["root_x"], window_details._data["root_y"]
        touch_window_type = window_details.child.get_full_property(display.intern_atom('_NET_WM_WINDOW_TYPE'), 0)
        if touch_window_type:
            touch_window_type = display.get_atom_name(touch_window_type.value[0])

        titles = getWindowTitles(window_details._data["child"])

        print(titles)

        if len(titles) != 0:
            if common_member(FIX_APPS, titles):
                fixflag = True
            else:
                fixflag = False

        print(fixflag)
        
        if event.value == 0 and touch_window_type in VALID_WINDOW_TYPES and not fixflag:
            fake_input(display, X.ButtonPress, left_click_button)
            fake_input(display, X.ButtonRelease, left_click_button)
            display.sync()

        
        if event.value == 1:
            time_a = time.time()
            pos_a = touch_pos
            
        if event.value == 0:
            time_b = time.time()
            pos_b = touch_pos

            print("time:", time_b - time_a)
            if time_b - time_a > 0.3:
                print("dst:", (pos_a[0]-pos_b[0])*(pos_a[0]-pos_b[0]) + (pos_a[1]-pos_b[1])*(pos_a[1]-pos_b[1]))
                if (pos_a[0]-pos_b[0])*(pos_a[0]-pos_b[0]) + (pos_a[1]-pos_b[1])*(pos_a[1]-pos_b[1]) < 2500:
                    print("right click detected")

                    if(common_member("chromium", titles)):
                        continue
                    
                    fake_input(display, X.ButtonPress, right_click_button)
                    fake_input(display, X.ButtonRelease, right_click_button)
                    display.sync()

    except:
        pass
