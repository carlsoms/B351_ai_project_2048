import tkinter as tk
from tkinter import *
from game import *

root = tk.Tk()
root.title("2048 Solver")

dict_words = {1: ("Play 2048", run_manual),
              2: ("Run Simple AI", run_simple_ai),
              3: ("Run Expectimax AI", run_expectimax)
              }
for k, j in dict_words.items():
    b = Button(root, width=20, text=j[0], command=j[1], background="#ece3cb", padx=5, pady=5)
    b.pack()

root.mainloop()
