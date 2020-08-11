from pynput.keyboard import Key, Controller, KeyCode
from pynput import keyboard
import time
from tkinter import *
import tkinter as tk

from typing import Optional
from ctypes import wintypes, windll, create_unicode_buffer

def getForegroundWindowTitle() -> Optional[str]:
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)

    # 1-liner alternative: return buf.value if buf.value else None
    if buf.value:
        return buf.value
    else:
        return None

root = tk.Tk()
root.title("Dan's Spam Manager")

# Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 2, weight=1)
# Grid.columnconfigure(root, 1, weight=1)
root.resizable(True,False)


#Create & Configure frame 
# frame=Frame(root)
# frame.grid(row=0, column=0, sticky=N+S+E+W)

def toggle():

    if toggle_btn.config('relief')[-1] == 'sunken':
        toggle_btn.config(relief="raised")
        listeners[-1].stop()
    else:
        toggle_btn.config(relief="sunken")
        listeners.append(keyboard.Listener(on_press=on_press))
        listeners[-1].start()

stringvars = []
stringentries = []
hotkeys = []
hotkeyentries = []


def addCommand():
    stringvars.append(StringVar())
    stringentries.append(Entry(root, textvariable=stringvars[-1]))
    hotkeys.append(StringVar())
    hotkeyentries.append(Entry(root, textvariable=hotkeys[-1]))
    for entry in stringentries:
        entry.grid(row=stringentries.index(entry) + 3,column=0,columnspan=3,sticky=W+E)
        if stringvars[stringentries.index(entry)].get() == "":
            stringvars[stringentries.index(entry)].set("default")
    for entry in hotkeyentries:
        entry.grid(row=hotkeyentries.index(entry) + 3,column=3,sticky=W+E)
        if hotkeys[hotkeyentries.index(entry)].get() == "":
            hotkeys[hotkeyentries.index(entry)].set("")

listeners = []

toggle_btn = tk.Button(text="Toggle", width=12, relief="raised", command=toggle)
toggle_btn.grid(row=0,column=0,pady=10,padx=10)
add_btn = tk.Button(text="Add a command", width=12, relief="raised", command=addCommand)
add_btn.grid(row=0,column=1)
tk.Label(text="Chat Button:").grid(row=1,column=0,pady=(0,10))
chatbutton = StringVar()
chatButtonEntry = Entry(root, textvariable=chatbutton)
chatButtonEntry.grid(row=1,column=1)
tk.Label(text="Text").grid(row=2,column=0)
tk.Label(text="Hotkey").grid(row=2,column=3)


def on_press(key):
    for phrase in stringvars:
        if getForegroundWindowTitle() != "Dan's Spam Manager":
            if key == keyboard.KeyCode.from_char(hotkeys[stringvars.index(phrase)].get()) or key == getattr(Key, hotkeys[stringvars.index(phrase)].get(), None):
                try:
                    Controller().press(chatbutton.get())
                except ValueError:
                    try:
                        Controller().press(getattr(Key, chatbutton.get()))
                    except AttributeError:
                        None
                try:
                    Controller().release(chatbutton.get())
                except ValueError:
                    try:
                        Controller().release(getattr(Key, chatbutton.get()))
                    except AttributeError:
                        None
                time.sleep(.1)
                Controller().type(phrase.get())
                time.sleep(.1)
                Controller().press(Key.enter)
                Controller().release(Key.enter)
                listeners[-1].stop()
                listeners.append(keyboard.Listener(on_press=on_press))
                listeners[-1].start()

addCommand()
root.mainloop()