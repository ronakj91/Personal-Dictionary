# -*- coding: utf-8 -*-
try:  # for Python2
    from Tkinter import *
    from tkMessageBox import showerror
    import ttk
    from tkinter import messagebox
    from tkinter import Scrollbar
    from ttk import Treeview
except ImportError:  # for Python3
    from tkinter import *
    from tkinter.messagebox import showerror
    from tkinter import ttk  # ttk = themed tkinter
    from tkinter import messagebox
    from tkinter import Scrollbar
    from tkinter.ttk import Treeview
import sqlite3
import traceback


class Database:
    def __init__(self, db_name):
        try:
            # Create a database or connect to already existing db file
            self.conn = sqlite3.connect(db_name)
            print("Connected to database successfully")
            # Create cursor
            self.cur = self.conn.cursor()
            self.cur.execute("CREATE TABLE IF NOT EXISTS dictionary(id integer PRIMARY KEY,Word text,Meaning text)")
            # Commit Changes
            self.conn.commit()

        except sqlite3.Error as error:
            print("Failed to create table", error)

    def fetch(self, word=''):
        self.cur.execute("SELECT * FROM dictionary WHERE Word LIKE ?", ('%' + word + '%',))
        rows = self.cur.fetchall()
        return rows

    def insert(self, word, meaning):
        # Insert into Table
        self.cur.execute("INSERT INTO dictionary VALUES (NULL, ?, ?)", (word, meaning))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM dictionary WHERE id=?", str(id))
        self.conn.commit()

    def remove_many(self, id_list):
        try:
            sqlite_update_query = """DELETE FROM dictionary WHERE id=?"""
            self.cur.executemany(sqlite_update_query, id_list)
            print("Total", self.cur.rowcount, "Records deleted successfully")
            self.conn.commit()
        except sqlite3.Error as error:
            print("Failed to delete multiple records from table", error)

    def update(self, id, word, meaning):
        self.cur.execute("UPDATE dictionary SET Word = ?, Meaning = ? WHERE id = ?",
                         (word, meaning, id))
        self.conn.commit()

    def __del__(self):
        # Close Connection
        self.conn.close()


class ConfigureGUI:
    """[summary]
    """

    def __init__(self, root):
        # Configure the root object for the Application
        self.root = root
        self.root.title(88 * " " + "GUI DICTIONARY")
        self.root.geometry("690x610+300+50")
        self.root.resizable(width=False, height=False)
        self.root.config(bg='#2A2C2B')

        # Create an instance of Database Class
        self.dbms_inst = Database("Dict_personal.db")

        # ================================VARIABLES============================
        self.word_to_add = StringVar()
        self.word_description = StringVar()

        # ================================FRAMES===============================
        # Create a Main Frame
        main_frame = Frame(self.root, bd=10, width=770, height=700,
                           relief=RIDGE, bg='cadet blue')
        main_frame.grid()

        # Create a Title Frame
        title_frame = Frame(main_frame, bd=7, padx=10, pady=10, width=770,
                            height=100, relief=RAISED)
        title_frame.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")

        # Create a Data Frame
        data_frame = Frame(main_frame, bd=5, width=770, height=700,
                           padx=10, pady=10, relief=RAISED)
        data_frame.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")

        # ======================LABEL WIDGET===================================
        self.lblWordToAdd = Label(title_frame, font=('Arial', 12, 'bold'),
                                  text="Enter your word ", fg="black",
                                  padx=1, pady=1, borderwidth=0)
        self.lblWordToAdd.grid(row=0, column=0, sticky=W)

        self.lblDescription = Label(title_frame, font=('Arial', 12, 'bold'),
                                    text="Enter description ", wraplength=500,
                                    padx=1, pady=1, borderwidth=0, fg="black")
        self.lblDescription.grid(row=1, column=0, sticky=W)

        # ======================ENTRY WIDGET===================================
        self.entWordToAdd = Entry(title_frame, font=('Arial', 12, 'bold'),
                                  textvariable=self.word_to_add,
                                  bd=5, justify='left', width=25)
        self.entWordToAdd.grid(row=0, column=1, sticky=W, padx=5)
        self.entDescription = Entry(title_frame, width=25, bd=5,
                                    font=('Arial', 12, 'bold'), justify='left',
                                    textvariable=self.word_description)
        self.entDescription.grid(row=1, column=1, sticky=W, padx=5)

        # ======================TREEVIEW WIDGET================================
        # Style the TreeView
        style = ttk.Style()
        # Use a theme
        style.theme_use("winnative")
        # Modify the font of the body
        style.configure('mystyle.Treeview', background="white", foreground="black",
                        rowheight=25, borderwidth='4', fieldbackground="white",
                        font=('Helvetica', 10))
        # Modify the font of the headings
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        # Change Selected Color
        style.map('mystyle.Treeview', background=[('selected', 'blue')])

        # Set the treeview
        self.word_database = ttk.Treeview(data_frame, height=15, style="mystyle.Treeview",
                                          selectmode="extended", show="headings")
        # Define our columns
        self.word_database['columns'] = ('Word', 'Meaning')

        # Adding Vertical Scrollbar to Treeview
        scroll_y = ttk.Scrollbar(data_frame, orient=VERTICAL,
                                 command=self.word_database.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.word_database.configure(yscrollcommand=scroll_y.set)

        # Adding Horizontal Scrollbar to Treeview
        scroll_x = Scrollbar(data_frame, orient=HORIZONTAL,
                             command=self.word_database.xview)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.word_database.configure(xscrollcommand=scroll_x.set)

        # Assigning the heading names to the respective columns
        self.word_database.heading("#0", text="", anchor=W)
        self.word_database.heading("Word", text="Keyword", anchor=W)
        self.word_database.heading("Meaning", text="Description", anchor=W)

        # Format the columns - Assign the width to respective columns
        self.word_database.column('#0', stretch='NO', minwidth=0, width=0)
        self.word_database.column("Word", stretch='YES', width=100, minwidth=80)
        self.word_database.column("Meaning", stretch='YES', width=500, minwidth=100)

        self.word_database.tag_configure('oddrow', background="lightblue")
        self.word_database.tag_configure('evenrow', background="white")

        # Calling pack method w.r.to treeview
        self.word_database.pack(side="left", fill=BOTH, expand=TRUE)

        # ====================== BUTTONS WIDGET===================================
        # Add Button
        add_button = Button(title_frame, text="Add Data", command=self.addData,
                            font=('Helvetica', 10, 'bold'), height=2, width=13, bd=4)
        add_button.grid(row=0, column=2, padx=2, pady=2, sticky="nsew")

        # Delete Button
        del_button = Button(title_frame, text="Delete Multiple",
                            font=('Helvetica', 10, 'bold'), height=2, width=13,
                            bd=4, command=self.deleteMultipleRecords)
        del_button.grid(row=1, column=2, padx=2, pady=2, sticky="nsew")

        # Search Button
        search_button = Button(title_frame, text="Search Data",
                               font=('Helvetica', 10, 'bold'), height=2,
                               width=13, bd=4, command=self.searchData)
        search_button.grid(row=0, column=3, padx=2, pady=2, sticky="nsew")

        # Update Button
        updt_button = Button(title_frame, text="Update Data",
                             font=('Helvetica', 10, 'bold'), height=2, width=13,
                             bd=4, command=self.updateData)
        updt_button.grid(row=1, column=3, padx=2, pady=2, sticky="nsew")

    # ======================FUNCTION DECLARATION===============================
    def populateView(self, word=''):
        self.word_database.delete(*self.word_database.get_children())
        global count
        count = 0
        for data in self.dbms_inst.fetch(word):
            print(data)  # print all records in the database
            # Add Data in the TreeView
            if count % 2 == 0:
                self.word_database.insert(parent='', index='end', text="", values=(data[1], data[2]),
                                          tags=('evenrow',))
            else:
                self.word_database.insert(parent='', index='end', text="", values=(data[1], data[2]),
                                          tags=('oddrow',))

            count += 1

    def addData(self):
        """
        Create a function to add a new record
        """
        word = self.entWordToAdd.get()
        meaning = self.entDescription.get()

        if word == "" or meaning == "":
            messagebox.showerror("Error", "Enter correct data !!")
        else:
            try:
                self.dbms_inst.insert(word, meaning)
            except Exception:
                messagebox.showinfo("Message", traceback.print_exc())
            finally:
                self.populateView()
                # Clear the Entry Boxes
                self.clearData()

    def deleteMultipleRecords(self):
        """
        Create a function to delete selected records
        """
        try:
            result = messagebox.askyesno("GUI Dictionary", "Are you sure you want to delete?",
                                         icon="warning", default='no')
            if result:  # True if OK button is clicked
                selected_rowid = self.word_database.selection()
                new_list = []
                for item in selected_rowid:
                    new_list.append(tuple([int(item[1:], 16)]))

                self.dbms_inst.remove_many(new_list)
                for record in selected_rowid:
                    self.word_database.delete(record)

        except Exception:
            messagebox.showinfo("Message", traceback.print_exc())
        finally:
            self.populateView()
            self.clearData()

    def clearData(self):
        self.entWordToAdd.delete(0, END)
        self.entDescription.delete(0, END)

    def searchData(self):
        word = self.entWordToAdd.get()
        self.populateView(word)

    def updateData(self):
        # Grab Record Number
        selected = self.word_database.focus()
        # Grab Record Values
        values = self.word_database.item(selected, 'values')

        # Output to Entry Boxes
        self.entWordToAdd.insert(0, values[0])
        self.entDescription.insert(0, values[1])

        # self.dbms_inst.update(selected, self.word_to_add.get(), self.word_description.get())

    def Exit_App(self):
        result = messagebox.askokcancel("Quit", "Are you sure you want to exit?", icon="warning")
        if result > 0:
            self.root.destroy()
            exit()


if __name__ == '__main__':
    window = Tk()
    window.wm_attributes('-fullscreen', 'false')
    application = ConfigureGUI(window)
    application.populateView()
    window.protocol('WM_DELETE_WINDOW', application.Exit_App)
    window.mainloop()
