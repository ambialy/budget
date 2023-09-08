import tkinter as tk
from tkinter import ttk
import tkcalendar
from datetime import datetime

class RocketBudget(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title('Rocket Budgeting')
        self.geometry('700x700')

        style = ttk.Style()
        style.theme_use('clam')

        self.notebook = ttk.Notebook(self)
        self.notebook.grid()

        self.frame_add_trans = ttk.Frame(self.notebook, width=680, height=680)
        self.frame_view_trans = ttk.Frame(self.notebook, width=680, height=680)

        self.frame_add_trans.grid()
        self.frame_view_trans.grid()

        # "title"
        self.lbl_trans = ttk.Label(self.frame_add_trans, text='Add a new transaction', background=None)
        self.lbl_trans.grid(column=1, row=0, pady=10)

        # calendar stuff
        self.cal = tkcalendar.Calendar(self.frame_add_trans, selectmode='day', year=datetime.today().year,
                month=datetime.today().month, day=datetime.today().day)
        self.cal.grid(column=1, row=2, pady=5)
        self.btn_date = ttk.Button(self.frame_add_trans, text='Select date', command=self.grab_date)
        self.btn_date.grid(column=1, row=3, pady=5)
        self.lbl_date = ttk.Label(self.frame_add_trans, text='Selected date: No date selected', foreground='red')
        self.lbl_date.grid(column=1, row=4, pady=4)

        # Get amount
        self.incomeVar = tk.BooleanVar()
        self.checkBoxIncome = ttk.Checkbutton(
            self.frame_add_trans, text='Income', command=None, variable=self.incomeVar,
            onvalue=True, offvalue=False).grid(column=2, row=5)
        self.lbl_amt = ttk.Label(self.frame_add_trans, text='Enter amount: ')
        self.lbl_amt.grid(column=0, row=5)
        self.amtVar = tk.DoubleVar()
        self.entry_amt = ttk.Entry(self.frame_add_trans, textvariable=self.amtVar)
        self.entry_amt.grid(column=1, row=5, pady=5)

        # Select Category
        self.lbl_category = ttk.Label(self.frame_add_trans, text='Choose category: ')
        self.lbl_category.grid(column=0, row=6)
        self.categoryVal = tk.StringVar()
        self.combo_category = ttk.Combobox(self.frame_add_trans, textvariable=self.categoryVal)
        # TODO replace with db query
        self.combo_category['values'] = ['Home', 'Personal', "Food", 'Home', 'Personal', "Food",
                    'Home', 'Personal', "Food", 'Home', 'Personal', "Food",
                    'Home', 'Personal', "Food", 'Home', 'Personal', "Food"]
        self.combo_category.state(['readonly'])
        self.combo_category.grid(column=1, row=6, pady=5)

        # note
        self.lbl_note = ttk.Label(self.frame_add_trans, text='Add a note (optional): ')
        self.lbl_note.grid(column=0, row=7)
        self.noteVar = tk.StringVar()
        self.entry_note = ttk.Entry(self.frame_add_trans, textvariable=self.noteVar)
        self.entry_note.grid(column=1, row=7, pady=5)

        # submit button
        # TODO write submit command
        self.btn_submit = ttk.Button(self.frame_add_trans, text='Submit', command=None)
        self.btn_submit.grid(column=1, row=8)

        # complie notebook
        self.notebook.add(self.frame_add_trans, text='Add Transaction')
        self.notebook.add(self.frame_view_trans, text='View Transactions')

    def grab_date(self):
        self.lbl_date.config(text=f"Selected date: {self.cal.get_date()}", foreground='black')

    def submit(self):
        pass

    def category_query(self):
        pass

if __name__ == "__main__":
    rb = RocketBudget()
    rb.mainloop()