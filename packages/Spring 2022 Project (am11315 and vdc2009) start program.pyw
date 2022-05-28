import os
import sys

abs_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(abs_path)
sys.path.insert(0, abs_path)
sys.path.insert(0, 'packages')
sys.path.append('tools')
from tkinter import filedialog
import py
import browse
import piano_config
import pyglet
import tkinter as tk
from tkinter import ttk

with open('Spring 2022 Project (am11315 and vdc2009).pyw', encoding='utf-8-sig') as f:
    exec(f.read())
