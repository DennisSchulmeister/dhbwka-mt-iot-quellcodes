#!/usr/bin/env python

import tkinter as tk

from tkinter import messagebox

def say_hello():
    """
    Zeigt eine Meldung mit dem Text "Hallo Welt!" an.
    """
    messagebox.showinfo("Hallo", "Hallo Welt!")

root = tk.Tk()

button = tk.Button(root, text="Click Me!", command=say_hello)
button.pack()

root.mainloop()
