from pynput.keyboard import Key, Controller, KeyCode
from pynput import keyboard
import time
from tkinter import *
import tkinter as tk

root = tk.Tk()

def toggle():

    if toggle_btn.config('relief')[-1] == 'sunken':
        toggle_btn.config(relief="raised")
        listeners[-1].stop()
    else:
        toggle_btn.config(relief="sunken")
        listeners.append(keyboard.Listener(on_press=on_press))
        listeners[-1].start()

# texts = []
stringvars = []
stringentries = []
hotkeys = []
hotkeyentries = []

# v = StringVar()
# e = Entry(root, textvariable=v)
# e.pack()

# v.set("a default value")

def addCommand():
    stringvars.append(StringVar())
    stringentries.append(Entry(root, textvariable=stringvars[-1]))
    hotkeys.append(StringVar())
    hotkeyentries.append(Entry(root, textvariable=hotkeys[-1]))
    for entry in stringentries:
        entry.grid(row=stringentries.index(entry) + 3,column=0)
        if stringvars[stringentries.index(entry)].get() == "":
            stringvars[stringentries.index(entry)].set("default")
    for entry in hotkeyentries:
        entry.grid(row=hotkeyentries.index(entry) + 3,column=1)
        if hotkeys[hotkeyentries.index(entry)].get() == "":
            hotkeys[hotkeyentries.index(entry)].set("add a hotkey")
    # texts.append()

listeners = []

toggle_btn = tk.Button(text="Toggle", width=12, relief="raised", command=toggle)
toggle_btn.grid(row=0,column=0)
add_btn = tk.Button(text="Add a command", width=12, relief="raised", command=addCommand)
add_btn.grid(row=0,column=1)
tk.Label(text="Chat Button =>").grid(row=1,column=0)
chatbutton = StringVar()
chatButtonEntry = Entry(root, textvariable=chatbutton)
chatButtonEntry.grid(row=1,column=1)
tk.Label(text="Text").grid(row=2,column=0)
tk.Label(text="Hotkey").grid(row=2,column=1)


def on_press(key):
    for phrase in stringvars:   
        if key == keyboard.KeyCode.from_char(hotkeys[stringvars.index(phrase)].get()):
            Controller().press(chatbutton.get())
            Controller().release(chatbutton.get())
            time.sleep(.1)
            Controller().type(phrase.get())
            time.sleep(.1)
            Controller().press(Key.enter)
            Controller().release(Key.enter)
    # try:
    #     print('alphanumeric key {0} pressed'.format(
    #         key.char))
    # except AttributeError:
    #     print('special key {0} pressed'.format(
    #         key))

# def on_release(key):
#     if key == keyboard.Key.esc:
#         # Stop listener
#         return False

# Collect events until released
addCommand()
root.mainloop()