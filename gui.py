import tkinter as tk
from tkinter import ttk
import tkcalendar
from datetime import datetime
import sqlite3

class RocketBudgeting(tk.Tk):

    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('RocketBudget.db')
        self.cur = self.conn.cursor()
        self.create_db()

        self.title('Rocket Budgeting')

        self.window_width, self.window_height = 700, 700
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        _x = int((self.screen_width/2) - (self.window_width/2))
        _y = int((self.screen_height/2) - (self.window_height/2))
        self.geometry(f'{self.window_width}x{self.window_height}+{_x}+{_y}')

        style = ttk.Style()
        style.theme_use('clam')

        self.notebook = ttk.Notebook(self)
        self.notebook.grid()

    def create_db(self):
        
        self.cur.execute("PRAGMA foreign_keys=on;")

        default_categories = ["Auto Parts & Service", "Books & Education", "Bills & Utilities", "Charity", "Coffee Shops", "Credit Card Payment",
                            "Dining & Drinks", "Entertainment & Recreation", "Family Care", "Fees", "Gas", "Gifts", "Golf", "Groceries",
                            "Health & Wellness", "Homecare & Supplies", "Income", "Interest Payment", "Investments", "Legal", "Loan Payment", "Medical",
                            "Mistake", "Personal Care", "Pets", "Recieved Gift", "Reimbursement", "Savings Transfer", "Shopping", "Software & Tech",
                            "Taxes", "Travel & Vacation"]


        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS _categories
                    (category TEXT NOT NULL PRIMARY KEY);
        """)


        # If the categories haven't been populated, fill them with the default values
        self.cur.execute("SELECT category FROM _categories")
        rows = self.cur.fetchone()
        if rows is None:
            for val in default_categories:
                self.cur.execute("INSERT INTO _categories VALUES (?)", (val,))
            
            self.conn.commit()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS _transactions 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    note TEXT,
                    recurring BOOLEAN,
                    FOREIGN KEY (category) REFERENCES _categories(category));
        """)

        self.conn.commit()

class AddTransaction():

    def __init__(self, master):
        self.master = master

        self.frame = ttk.Frame(self.master.notebook, width=700, height=680)
        self.frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        
        # "title"
        self.lbl_trans = ttk.Label(self.frame, text='Add a new transaction', background=None)
        self.lbl_trans.grid(column=1, row=0, pady=10)

        # calendar stuff
        self.cal = tkcalendar.Calendar(self.frame, selectmode='day', year=datetime.today().year,
                month=datetime.today().month, day=datetime.today().day)
        self.cal.grid(column=1, row=2, pady=5)
        self.btn_date = ttk.Button(self.frame, text='Select date', command=self.grab_date)
        self.btn_date.grid(column=1, row=3, pady=5)
        self.lbl_date = ttk.Label(self.frame, text='Selected date: No date selected', foreground='red')
        self.lbl_date.grid(column=1, row=4, pady=4)

        # recurring check
        self.recurringVar = tk.BooleanVar()
        self.checkBoxRecurring = ttk.Checkbutton(
            self.frame, text='Recurring', command=None, variable=self.recurringVar,
            onvalue=True, offvalue=False).grid(column=3, row=5)
        
        # Get amount
        self.lbl_amt = ttk.Label(self.frame, text='Enter amount: $')
        self.lbl_amt.grid(column=0, row=5, sticky=tk.E)
        self.amtVar = tk.DoubleVar()
        self.entry_amt = ttk.Entry(self.frame, textvariable=self.amtVar)
        self.entry_amt.grid(column=1, row=5, pady=5)

        # Select Category
        self.lbl_category = ttk.Label(self.frame, text='Choose category: ')
        self.lbl_category.grid(column=0, row=6)
        self.categoryVal = tk.StringVar()
        self.combo_category = ttk.Combobox(self.frame, textvariable=self.categoryVal)
        _categories = self.master.cur.execute("SELECT category FROM _categories")
        cats = list(_categories.fetchall())
        cat_list = [cat[0] for cat in cats]
        self.combo_category['values'] = cat_list
        self.combo_category.state(['readonly'])
        self.combo_category.grid(column=1, row=6, pady=5)

        # note
        self.lbl_note = ttk.Label(self.frame, text='Add a note (optional): ')
        self.lbl_note.grid(column=0, row=7)
        self.noteVar = tk.StringVar()
        self.entry_note = ttk.Entry(self.frame, textvariable=self.noteVar)
        self.entry_note.grid(column=1, row=7, pady=5)

        # submit button
        # TODO write submit command
        self.btn_submit = ttk.Button(self.frame, text='Submit', command=self.submit_transaction)
        self.btn_submit.grid(column=1, row=8)
        self.lbl_success = ttk.Label(self.frame, text='', foreground='green')
        self.lbl_success.grid(column=1, row=9, pady=5)


        self.master.notebook.add(self.frame, text='Add Transaction')
    

    def grab_date(self):
        self.lbl_date.config(text=f"Selected date: {self.cal.get_date()}", foreground='black')


    def submit_transaction(self):
        try:
            date = self.cal.get_date()
            amount = self.entry_amt.get()
            category = self.combo_category.get()
            note = self.entry_note.get()
            recurring = self.recurringVar.get()

            self.master.cur.execute("INSERT INTO _transactions VALUES (?, ?, ?, ?, ?, ?)", (None, date, amount, category, note, recurring))
            self.master.conn.commit()

            self.lbl_success.config(text=f'Transaction on {date} for ${amount} successfully added', foreground='green')
            self.entry_amt.delete(0, tk.END)
            self.combo_category.set("")
            self.entry_note.delete(0, tk.END)
            
        except sqlite3.Error as e:
            self.lbl_success.config(text=f'Transaction errored: {e}', foreground='red')

class ViewTransactions():

    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master.notebook, width=700, height=680)
        self.frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))


        self.master.notebook.add(self.frame, text='View Transactions')

class EditCategories():

    def __init__(self, master):
        self.master = master

        self.frame = ttk.Frame(self.master.notebook, width=700, height=680)
        self.frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        # Select Category
        self.lbl_category = ttk.Label(self.frame, text='Choose category: ')
        self.lbl_category.grid(column=0, row=1)
        self.categoryVal = tk.StringVar()
        self.combo_category = ttk.Combobox(self.frame, textvariable=self.categoryVal)
        self._categories = self.master.cur.execute("SELECT category FROM _categories")
        self.cats = list(self._categories.fetchall())
        self.cat_list = [cat[0] for cat in self.cats]
        self.combo_category['values'] = self.cat_list
        self.combo_category.state(['readonly'])
        self.combo_category.grid(column=1, row=1, pady=5)


        # Delete button
        self.btn_submit = ttk.Button(self.frame, text='Delete', command=self.delete_transaction)
        self.btn_submit.grid(column=2, row=1)
        self.lbl_success = ttk.Label(self.frame, text='', foreground='green')
        self.lbl_success.grid(column=1, row=2, pady=5)


        self.master.notebook.add(self.frame, text='Edit Categories')

    def delete_transaction(self):
        category = self.combo_category.get()
        default_categories = ["Auto Parts & Service", "Books & Education", "Bills & Utilities", "Charity", "Coffee Shops", "Credit Card Payment",
                                "Dining & Drinks", "Entertainment & Recreation", "Family Care", "Fees", "Gas", "Gifts", "Golf", "Groceries",
                                "Health & Wellness", "Homecare & Supplies", "Income", "Interest Payment", "Investments", "Legal", "Loan Payment", "Medical",
                                "Mistake", "Personal Care", "Pets", "Recieved Gift", "Reimbursement", "Savings Transfer", "Shopping", "Software & Tech",
                                "Taxes", "Travel & Vacation"]
        
        if category in default_categories:
            self.lbl_success.config(text='You cannot delete a default category', foreground='red')        
        else:
            try:
                self.master.cur.execute("DELETE FROM _categories WHERE category=?", (category, ))
                self.master.conn.commit()
                self.lbl_success.config(text=f'Successfully deleted category {category}', foreground='green')
                self.combo_category.set("")
                self._categories = self.master.cur.execute("SELECT category FROM _categories")
                self.cats = list(self._categories.fetchall())
                self.cat_list = [cat[0] for cat in self.cats]
                self.combo_category['values'] = self.cat_list
                self.combo_category.state(['readonly'])
                
            except sqlite3.Error as e:
                self.lbl_success.config(text=f'Transaction errored: {e}', foreground='red')

if __name__ == "__main__":
    rb = RocketBudgeting()
    AddTransaction(rb)
    ViewTransactions(rb)
    EditCategories(rb)
    rb.mainloop()