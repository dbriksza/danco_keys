from pynput.keyboard import Key, Controller, KeyCode
from pynput import keyboard
import time
from tkinter import *
import tkinter as tk

from typing import Optional
from ctypes import wintypes, windll, create_unicode_buffer

class Counter():
    def __init__(self):
        self.counter = 0

    def increment(self):
        self.counter += 1

    def reset(self):
        self.counter = 0

    def get_value(self):
        return self.counter

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

def toggleAuto(btn):
    if autoentries[btn].config('relief')[-1] == 'sunken':
        autoentries[btn].config(relief='raised')
    elif autoentries[btn].config('relief')[-1] == 'raised':
        autoentries[btn].config(relief='sunken')
    if holdentries[btn].config('relief')[-1] == 'sunken':
        holdentries[btn].config(relief='raised')
    elif holdentries[btn].config('relief')[-1] == 'raised':
        holdentries[btn].config(relief='sunken')

stringvars = []
stringentries = []
hotkeys = []
hotkeyentries = []

delays = []
delayentries = []

autoindexer = Counter()

autos = []
autoentries = {}

holdindexer = Counter()

holds = []
holdentries = {}

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

def addAuto():
    autoindexer.increment()
    buttonindex = autoindexer.get_value()
    autos.append(buttonindex)
    delays.append(StringVar())
    delayentries.append(Entry(root, textvariable=delays[-1]))
    autoentries[buttonindex] = tk.Button(text="toggle", width=12, relief="raised", command=lambda: toggleAuto(buttonindex))
    autoentries[buttonindex].grid(row=len(autoentries) + 2,column=4,sticky=W+E)
    for entry in delayentries:
        entry.grid(row=delayentries.index(entry) + 3,column=5,sticky=W+E)
        if delays[delayentries.index(entry)].get() == "":
            delays[delayentries.index(entry)].set("500")

def addHold():
    holdindexer.increment()
    buttonindex = holdindexer.get_value()
    holds.append(buttonindex)
    holdentries[buttonindex] = tk.Button(text="toggle", width=12, relief="raised", command=lambda: toggleAuto(buttonindex))
    holdentries[buttonindex].grid(row=len(autoentries) + 2,column=6,sticky=W+E)

listeners = []

toggle_btn = tk.Button(text="Toggle", width=12, relief="raised", command=toggle)
toggle_btn.grid(row=0,column=0,pady=10,padx=10)
add_btn = tk.Button(text="Add a command", width=12, relief="raised", command=lambda: [addCommand(), addAuto()])
add_btn.grid(row=0,column=1)
tk.Label(text="Chat Button:").grid(row=1,column=0,pady=(0,10))
chatbutton = StringVar()
chatButtonEntry = Entry(root, textvariable=chatbutton)
chatButtonEntry.grid(row=1,column=1)
tk.Label(text="Text").grid(row=2,column=0)
tk.Label(text="Hotkey").grid(row=2,column=3)
tk.Label(text="Repeat:").grid(row=2,column=4,pady=(0,10))
tk.Label(text="Delay:").grid(row=2,column=5,pady=(0,10))

timetostop = {}

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
                if autoentries[stringvars.index(phrase) + 1].config('relief')[-1] == 'sunken' and (key not in timetostop or timetostop[key] == 'off'):
                    timetostop[key] = 'on'
                    listeners[-1].stop()
                    listeners.append(keyboard.Listener(on_press=on_press))
                    listeners[-1].start()
                    while timetostop[key] == 'on':
                        Controller().type(phrase.get())
                        time.sleep(int(delays[stringvars.index(phrase)].get()) / 1000)
                elif timetostop.get(key, None) == 'on':
                    timetostop[key] = 'off'
                else: 
                    time.sleep(.1)
                    Controller().type(phrase.get())
                    time.sleep(.1)
                    Controller().press(Key.enter)
                    Controller().release(Key.enter)
                    active = 0
                    listeners[-1].stop()
                    listeners.append(keyboard.Listener(on_press=on_press))
                    listeners[-1].start()
                    

addAuto()
addCommand()
addHold()
root.mainloop()