# -*- coding: utf-8 -*-
import sqlite3
import traceback
from sqlite3 import Error
from tkinter import *
from tkinter import ttk, Scrollbar, messagebox


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS dictionary(id integer PRIMARY KEY,Word text,Meaning text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM dictionary")
        rows = self.cur.fetchall()
        return rows

    def insert(self, word, meaning):
        self.cur.execute("INSERT INTO dictionary VALUES (NULL, ?, ?)", (word, meaning))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM dictionary WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, word, meaning):
        self.cur.execute("UPDATE dictionary SET word = ?, meaning = ? WHERE id = ?",
                         (word, meaning, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()


class ConfigureGUI():
    """[summary]
    """

    def __init__(self, root):
        # Configure the root object for the Application
        self.root = root
        self.root.title(102 * " " + "GUI DICTIONARY")
        self.root.geometry("720x770+300+0")
        self.root.resizable(width=False, height=False)
        self.root.config(background="silver")

        # Create an instance of Database Class
        self.dbms_inst = Database("Dict_personal.db")

        # ======================VARIABLES==============================
        word_to_add = StringVar()
        word_description = StringVar()
        self.id = 1
        self.iid = 0

        # ======================FRAMES==============================
        # Create a Main Frame
        main_frame = Frame(self.root, bd=10, width=770, height=700,
                           relief=RIDGE, bg='cadet blue')
        main_frame.grid()

        # Create a Title Frame
        title_frame = Frame(main_frame, bd=7, padx=10, pady=10, width=770,
                            height=100, relief=RIDGE)
        title_frame.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")

        # Create a Data Frame
        data_frame = Frame(main_frame, bd=5, width=770, height=700,
                           padx=10, pady=10, relief=RAISED)
        data_frame.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")

        # ======================LABEL WIDGET=============================
        self.lblWordToAdd = Label(title_frame, font=('Arial', 12, 'bold'),
                                  text="Enter your word ",
                                  padx=2, pady=2, borderwidth=0)
        self.lblWordToAdd.grid(row=0, column=0, sticky=W, padx=5)

        self.lblDescription = Label(title_frame, font=('Arial', 12, 'bold'),
                                    text="Enter description ",
                                    padx=2, pady=2, borderwidth=0)
        self.lblDescription.grid(row=1, column=0, sticky=W, padx=5)

        # ======================ENTRY WIDGET===================================
        self.entWordToAdd = Entry(title_frame, font=('Arial', 12, 'bold'),
                                  textvariable=word_to_add,
                                  bd=5, justify='left', width=25)
        self.entWordToAdd.grid(row=0, column=1, sticky=W, padx=5)
        self.entDescription = Entry(title_frame, width=25, bd=5,
                                    font=('Arial', 12, 'bold'), justify='left',
                                    textvariable=word_description)
        self.entDescription.grid(row=1, column=1, sticky=W, padx=5)

        # ======================TREEVIEW WIDGET================================
        db_columns = ['id', 'Word', 'Meaning']
        # Set the treeview
        self.word_database = ttk.Treeview(data_frame, height=50,
                                          selectmode="extended",
                                          columns=db_columns)

        # Adding Vertical Scrollbar to Treeview
        scroll_y = Scrollbar(data_frame, orient=VERTICAL,
                             command=self.word_database.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.word_database.configure(yscrollcommand=scroll_y.set)

        # Adding Horizontal Scrollbar to Treeview
        scroll_x = Scrollbar(data_frame, orient=HORIZONTAL,
                             command=self.word_database.xview)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.word_database.configure(xscrollcommand=scroll_x.set)

        # Assigning the heading names to the respective columns
        self.word_database.heading("#0", text="Sr No", anchor=W)
        self.word_database.heading("#1", text="Keyword", anchor=W)
        self.word_database.heading("#2", text="Description", anchor=W)

        # Assigning the width to respective columns
        self.word_database.column('#0', stretch='NO', minwidth=50, width=50)
        self.word_database.column("#1", stretch='NO', width=100, minwidth=80)
        self.word_database.column("#2", stretch='NO', width=500, minwidth=100)

        # Calling pack method w.r.to treeview
        self.word_database.pack(side='top', fill=BOTH, expand=1)

        # ======================BUTTONS WIDGET===================================
        # Add Button
        add_button = Button(title_frame, text="Add Data", command=self.addData,
                            font=('Arial', 8, 'bold'), height=2, width=10, bd=4)
        add_button.grid(row=0, column=2, padx=2, pady=2, sticky="nsew")

        # Delete Button
        del_button = Button(title_frame, text="Delete Data",
                            font=('Arial', 8, 'bold'), height=2, width=10,
                            bd=4, command=self.delete_data)
        del_button.grid(row=1, column=2, padx=2, pady=2, sticky="nsew")

        # Search Button
        search_button = Button(title_frame, text="Search Data",
                               font=('Arial', 8, 'bold'), height=2, width=10,
                               bd=4, command=self.searchData)
        search_button.grid(row=0, column=3, padx=2, pady=2, sticky="nsew")

        # Clear Button
        clr_button = Button(title_frame, text="Clear Data",
                            font=('Arial', 8, 'bold'), height=2, width=10,
                            bd=4, command=self.clearData)
        clr_button.grid(row=1, column=3, padx=2, pady=2, sticky="nsew")

        # Exit Button
        exit_button = Button(title_frame, text="Exit",
                             font=('Arial', 8, 'bold'), height=2, width=10,
                             bd=4, command=self.Exit_App)
        exit_button.grid(row=1, column=4, padx=2, pady=2, sticky="nsew")

    # ======================FUNCTION DECLARATION===============================
    def populateView(self):
        self.word_database.delete(*self.word_database.get_children())
        for data in self.dbms_inst.fetch():
            print(data)  # print all records in the database
            self.word_database.insert(parent='', index='end', iid=self.iid,
                                      text=self.id, values=(data[1], data[2]))
            self.id += 1
            self.iid += 1

    def addData(self):
        word = self.entWordToAdd.get()
        meaning = self.entDescription.get()

        if word == "" or meaning == "":
            messagebox.showerror("Error", "Enter correct data !!")
            return
        else:
            try:
                self.dbms_inst.insert(word, meaning)
                messagebox.showinfo("GUI Dictionary", "Record Added")
            except Exception:
                messagebox.showinfo("Message", traceback.print_exc())
            finally:
                self.clearData()
                self.populateView()

    def delete_data(self):
        row_id = int(self.word_database.focus())
        result = messagebox.askyesno("GUI Dictionary",
                                     "Are you sure you want to delete?", icon="warning")
        if result > 0:
            self.word_database.delete(row_id)

    def clearData(self):
        self.entWordToAdd.delete(0, END)
        self.entDescription.delete(0, END)

    def searchData(self):
        pass

    def Exit_App(self):
        result = messagebox.askyesno("GUI Dictionary",
                                     "Do you want to exit?", icon="warning")
        if result > 0:
            self.root.destroy()
            exit()


if __name__ == '__main__':
    window = Tk()
    application = ConfigureGUI(window)
    application.populateView()
    # Start program
    window.mainloop()
