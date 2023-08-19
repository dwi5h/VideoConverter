from tkinter import *
import os

def SwitchButton(button, state):
    button.config(state=state)

def FileCount(folder_path_input):
    fileCount = 0;
    
    dir = folder_path_input.get()
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, path)):
            split = os.path.splitext(path)
            if split[1] == ".ts":
                fileCount += 1
    
    return fileCount