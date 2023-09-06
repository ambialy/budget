import tkinter as tk
from tkinter import ttk
import tkcalendar
from datetime import datetime

root = tk.Tk()
root.title("Rocket Budgeting")

# frame = ttk.Frame(root)

# want a 6x4 grid window

lbl_transaction = ttk.Label(root, text="Add a new transaction")
# lbl_transaction.grid(row=0, column=0, columnspan=4)
lbl_transaction.pack(pady=10)

style = ttk.Style()
style.theme_use('clam')  # -> uncomment this line if the styling does not work

# Old calendar stuff
cal = tkcalendar.Calendar(root, selectmode='day', year=datetime.today().year,
                month=datetime.today().month, day=datetime.today().day)
cal.pack()

def grab_date():
    lbl_date.config(text=cal.get_date())

butt_date = tk.Button(root, text="Select date", command=grab_date)
butt_date.pack()
lbl_date = tk.Label(root, text='')

amountVar = tk.DoubleVar()
entry_amount = tk.Entry(root, textvariable=amountVar)
entry_amount.pack(pady=5)

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