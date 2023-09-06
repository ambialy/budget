import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Rocket Budgeting")

for i in range(6):
    root.columnconfigure(i, weight=1)
    root.rowconfigure(i, weight=i)

    for j in range(4):
        frame = tk.Frame(master=root)
        frame.grid(row=i, column=j, padx=5, pady=5)
        label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
        label.pack(padx=5, pady=5)



# ***** Menubar stuff *********
menubar = tk.Menu(root)
root.config(menu=menubar)

menu_file = tk.Menu(menubar)
menu_file.add_command(
    label='Exit',
    command=root.destroy
)

menubar.add_cascade(
    label='File',
    menu=menu_file
)
# ***** Menubar stuff *********

root.mainloop()