import tkinter as tk
from tkinter import ttk
import tkcalendar
from datetime import datetime
import sqlite3

class RocketBudget(tk.Tk):

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

        self.frame_add_trans = ttk.Frame(self.notebook, width=700, height=680)
        self.frame_view_trans = ttk.Frame(self.notebook, width=700, height=680)
        self.frame_recurring_trans = ttk.Frame(self.notebook, width=700, height=680)

        self.frame_add_trans.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.frame_view_trans.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

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

        # recurring check
        self.recurringVar = tk.BooleanVar()
        self.checkBoxRecurring = ttk.Checkbutton(
            self.frame_add_trans, text='Recurring', command=None, variable=self.recurringVar,
            onvalue=True, offvalue=False).grid(column=3, row=5)

        # Get amount
        self.incomeVar = tk.BooleanVar()
        self.checkBoxIncome = ttk.Checkbutton(
            self.frame_add_trans, text='Income', command=self.set_income_categories, variable=self.incomeVar,
            onvalue=True, offvalue=False).grid(column=2, row=5, sticky=tk.W)
        self.lbl_amt = ttk.Label(self.frame_add_trans, text='Enter amount: $')
        self.lbl_amt.grid(column=0, row=5, sticky=tk.E)
        self.amtVar = tk.DoubleVar()
        self.entry_amt = ttk.Entry(self.frame_add_trans, textvariable=self.amtVar)
        self.entry_amt.grid(column=1, row=5, pady=5)

        # Select Category
        self.lbl_category = ttk.Label(self.frame_add_trans, text='Choose category: ')
        self.lbl_category.grid(column=0, row=6)
        self.categoryVal = tk.StringVar()
        self.combo_category = ttk.Combobox(self.frame_add_trans, textvariable=self.categoryVal)
        _categories = self.cur.execute("SELECT category FROM _categories")
        cats = list(_categories.fetchall())
        cat_list = [cat[0] for cat in cats]
        self.combo_category['values'] = cat_list
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
        self.btn_submit = ttk.Button(self.frame_add_trans, text='Submit', command=self.submit_transaction)
        self.btn_submit.grid(column=1, row=8)
        self.lbl_success = ttk.Label(self.frame_add_trans, text='', foreground='green')
        self.lbl_success.grid(column=1, row=9, pady=5)

        # complie notebook
        self.notebook.add(self.frame_add_trans, text='Add Transaction')
        self.notebook.add(self.frame_view_trans, text='View Transactions')
        self.notebook.add(self.frame_recurring_trans, text='View Recurring')

    def set_income_categories(self):
        if self.incomeVar.get():
            self.combo_category['values'] = ['Income']
        else:
            self.combo_category['values'] = ['Home', 'Personal', "Food", 'Home', 'Personal', "Food",
                'Home', 'Personal', "Food", 'Home', 'Personal', "Food",
                'Home', 'Personal', "Food", 'Home', 'Personal', "Food"]  
    
    def submit_transaction(self):
        try:
            date = self.cal.get_date()
            amount = self.entry_amt.get()
            category = self.combo_category.get()
            note = self.entry_note.get()
            recurring = self.recurringVar.get()

            self.cur.execute("INSERT INTO _transactions VALUES (?, ?, ?, ?, ?, ?)", (None, date, amount, category, note, recurring))
            self.conn.commit()

            self.lbl_success.config(text=f'Transaction on {date} for ${amount} successfully added', foreground='green')
            self.entry_amt.delete(0, tk.END)
            self.combo_category.set("")
            self.entry_note.delete(0, tk.END)
            
        except sqlite3.Error as e:
            self.lbl_success.config(text=f'Transaction errored: {e}', foreground='red')
        

    def grab_date(self):
        self.lbl_date.config(text=f"Selected date: {self.cal.get_date()}", foreground='black')

    def submit(self):
        pass

    def category_query(self):
        pass

    def create_db(self):
        
        self.cur.execute("PRAGMA foreign_keys=on;")

        default_categories = ["Auto Parts & Service", "Books & Education", "Bills & Utilities", "Charity", "Coffee Shops", "Credit Card Payment",
                            "Dining & Drinks", "Entertainment & Recreation", "Family Care", "Fees", "Gas", "Gifts", "Golf", "Groceries",
                            "Health & Wellness", "Homecare & Supplies", "Ignore", "Investments", "Legal", "Loan Payment",
                            "Medical", "Mistake", "Personal Care", "Pets", "Reimbursement", "Savings Transfer", "Shopping", "Software & Tech",
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

        # self.cur.execute("DROP TABLE _transactions")

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


if __name__ == "__main__":
    rb = RocketBudget()
    rb.mainloop()