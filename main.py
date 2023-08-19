from asyncio import subprocess
from operator import truediv
from pydoc import Helper
from re import I
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import subprocess
from subprocess import Popen, PIPE
from threading import Thread
import helper
from numpy import full
import time

root = Tk()
frm = ttk.Frame(root, padding=50)

def browse_button_input():
    global folder_path_input
    filename = filedialog.askdirectory()
    if filename == "":
        folder_path_input.set("Pilih Folder Input")
    else:
        folder_path_input.set(filename)

def browse_button_output():
    global folder_path_output
    filename = filedialog.askdirectory()
    if filename == "":
        folder_path_output.set("Pilih Folder Output")
    else:
        folder_path_output.set(filename)

def StartConvert():
    if folder_path_input.get() == "Pilih Folder Input" and folder_path_output.get() == "Pilih Folder Output":
        status.set("Pilih folder input dan folder output dulu!")
    else:
        helper.SwitchButton(btnConvert, "disabled")
        helper.SwitchButton(btnInput, "disabled")
        helper.SwitchButton(btnOutput, "disabled")
        helper.SwitchButton(btnStop, "enable")
        # Thread(target = Convert).start()
        global th, stop
        stop = False
        th = Thread(target = Convert)
        th.start()

def Convert():
    count = helper.FileCount(folder_path_input)
    status.set(f"Converting (0/{count})")
    proses = 0;
    
    dir = folder_path_input.get()
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, path)):
            split = os.path.splitext(path)
            if split[1] == ".ts":
                fullPath = f"{dir}/{path}"
                subprocess.call(f"ffmpeg -y -i \"{fullPath}\" -c copy \"{folder_path_output.get()}/{split[0]}.mkv\"", shell=True)
                proses += 1
                status.set(f"Converting ({proses}/{count})")
                global stop
                if stop:
                    break
                
    status.set(f"Success ({proses}/{count})")
    helper.SwitchButton(btnConvert, "enable")
    helper.SwitchButton(btnInput, "enable")
    helper.SwitchButton(btnOutput, "enable")
    helper.SwitchButton(btnStop, "disabled")

def StopConvert():
    global stop
    stop = True

stop = False
th = Thread(target = Convert)

frm.grid()
status = StringVar()

folder_path_input = StringVar()
folder_path_input.set("Pilih Folder Input")

folder_path_output = StringVar()
folder_path_output.set("Pilih Folder Output")

ttk.Label(frm, text="== AUTO CONVERT .ts to .mkv ==").grid(column=1, columnspan=2, row=10, pady=(0, 25))

ttk.Label(frm, textvariable=folder_path_input).grid(column=1, row=50)
btnInput = ttk.Button(frm, text="Browse Folder", command=browse_button_input)
btnInput.grid(column=2, row=50)

ttk.Label(frm, textvariable=folder_path_output).grid(column=1, row=51)
btnOutput = ttk.Button(frm, text="Browse Folder", command=browse_button_output)
btnOutput.grid(column=2, row=51)

labelStatus = ttk.Label(frm, textvariable=status)
labelStatus.grid(column=1, columnspan=2, row=99, pady=(50, 5))

btnConvert = ttk.Button(frm, text="Convert", command=StartConvert)
btnConvert.grid(column=1, row=100)

btnStop = ttk.Button(frm, text="Stop", command=StopConvert)
btnStop.grid(column=2, row=100)
helper.SwitchButton(btnStop, "disabled")

root.mainloop()