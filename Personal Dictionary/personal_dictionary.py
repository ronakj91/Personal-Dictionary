# -*- coding: utf-8 -*-
try:  # for Python2
    from tkinter import *
    from tkinter import ttk,messagebox,Scrollbar,filedialog
    from tkinter.ttk import Treeview
except ImportError:  # for Python3
    from tkinter import *
    from tkinter import ttk ,messagebox,Scrollbar,filedialog
    from tkinter.ttk import Treeview
import sqlite3
import traceback
import csv
import os
import logging


class Database:
    def __init__(self, db_name):
        try:
            # Create a database or connect to already existing db file
            self.conn = sqlite3.connect(db_name)
            print("Connected to database successfully")
            # Creating a cursor object using the cursor() method
            self.cur = self.conn.cursor()
            self.cur.execute("""CREATE TABLE IF NOT EXISTS dictionary(id integer PRIMARY KEY,Word text,Meaning text)""")
            # Commit Changes
            self.conn.commit()

        except sqlite3.Error as error:
            print("Failed to create table", error)
        finally:
            #return the last changes made to the database
            self.conn.rollback()

    def fetch(self, word=''):
        try:
            # Search into Table
            self.cur.execute("SELECT * FROM dictionary WHERE Word LIKE ?", ('%' + word + '%',))
            records  = self.cur.fetchall()
            return records 

        except sqlite3.Error as error:
            print("Failed to search records from table", error)

    def insert(self, word, meaning):
        # Insert into Table
        self.cur.execute("INSERT INTO dictionary VALUES (NULL, ?, ?)", (word, meaning))
        self.conn.commit()

    def remove_many(self, id_list):
        try:
            self.cur.executemany("""DELETE FROM dictionary WHERE id=?""", [(a,) for a in id_list])
            print("Total", self.cur.rowcount, "Records deleted successfully")
            self.conn.commit()
            id_list=[]
        except sqlite3.Error as error:
            print("Failed to delete multiple records from table", error)
        finally:
            self.conn.rollback()

    def update(self, id_number, word, meaning):
        try:
            # Execute the SQL command to update values in database
            self.cur.execute("UPDATE dictionary SET Word=?, Meaning=? WHERE id=?",(word, meaning, id_number))

            # Commit your changes in the database
            self.conn.commit()
            self.cur.execute('''SELECT * from dictionary''')

            #Displaying the result
            print(self.cur.fetchall())
        except sqlite3.Error as error:
            print("Failed to update records from dictionary", error)
        finally:
            #return the last changes made to the database
            self.conn.rollback()

    def __del__(self):
        # Close Connection
        if self.conn is not None:
            self.conn.close()

class ConfigureGUI:
    """[summary]
    """

    def __init__(self, root):
        # Configure the root object for the Application
        self.root = root
        self.root.title(88 * " " + "GUI DICTIONARY")
        #self.root.geometry("717x700+300+50")
        self.root.geometry("")
        self.root.resizable(width=False, height=False)
        self.root.config(bg='#2A2C2B')

        # ================================Creating Menu Object============================
        my_menu = Menu(root)
        self.root.config(menu=my_menu)

        #Create a File Menu Item
        file_menu = Menu(my_menu)
        my_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open",command=self.importcsv)
        file_menu.add_command(label="Save",command=self.exportcsv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit",command=self.Exit_App)

        #Create a Edit Menu Item
        edit_menu = Menu(my_menu)
        my_menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_command(label="Paste")

        #Create a About Menu Item
        about_menu = Menu(my_menu)
        my_menu.add_cascade(label="About", menu=about_menu)

        # Create an instance of Database Class
        self.dbms_inst = Database("Dict_personal.db")

        # ================================VARIABLES============================
        self.word_to_add = StringVar()
        self.word_description = StringVar()
        self.name_to_search = StringVar()

        # ================================FRAMES===============================
        # Create a Main Frame
        main_frame = Frame(self.root, bd=10, width=770, height=700,
                           relief=RIDGE, bg='cadet blue')
        main_frame.grid()

        # Create a Title Frame
        title_frame = Frame(main_frame, bd=7, padx=10, pady=10, width=770,
                            height=100, relief=RAISED)
        title_frame.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")

        # Create a Treeview Frame with scrollable frame
        tree_frame  = Frame(main_frame, bd=5, width=770, height=700,
                           padx=10, pady=10, relief=RAISED)
        tree_frame.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")

        # Create a search bar Frame
        label_frame = Frame(main_frame, bd=7, padx=10, pady=10, width=770,
                            height=50, relief=RAISED)
        label_frame.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")

        # ======================LABEL WIDGET===================================    
        self.ws_lbl = Label(label_frame, text = "Search Keyword", font=('Arial', 12, 'bold'), 
                            fg="black",padx=1, pady=1, borderwidth=0)
        self.ws_lbl.grid(row=0, column=0, sticky=W)
  
        self.lblWordToAdd = Label(title_frame, font=('Arial', 12, 'bold'),
                                  text="Enter Keyword ", fg="black",
                                  padx=1, pady=1, borderwidth=0)
        self.lblWordToAdd.grid(row=0, column=0, sticky=W)

        self.lblDescription = Label(title_frame, font=('Arial', 12, 'bold'),
                                    text="Enter Description ", wraplength=500,
                                    padx=1, pady=1, borderwidth=0, fg="black")
        self.lblDescription.grid(row=1, column=0, sticky=W)

        # ======================ENTRY WIDGET===================================
        self.ws_ent = Entry(label_frame, textvariable=self.name_to_search,bd=5, justify='left',
                            width = 40, font=('Arial', 12, 'bold'))
        self.ws_ent.grid(row=0, column=1, sticky=W, padx=5)

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
        # Configure the Treeview Colors
        style.configure('mystyle.Treeview', background="white", foreground="black",
                        rowheight=25, borderwidth='4', fieldbackground="white",
                        font=('Helvetica', 10))
        # Modify the font of the headings
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))

        # Change Selected Color
        style.map('mystyle.Treeview', background=[('selected', 'blue')])

        # Set the treeview
        self.word_database = ttk.Treeview(tree_frame, height=15, style="mystyle.Treeview",
                                          selectmode="extended", show="headings")
        # Define our columns
        self.word_database['columns'] = ('ID','Word', 'Meaning')

        # Adding Horizontal Scrollbar to Treeview
        scroll_x = ttk.Scrollbar(tree_frame, orient=HORIZONTAL,command=self.word_database.xview)
        scroll_x.pack(side=BOTTOM, fill='x')

        # Adding Vertical Scrollbar to Treeview
        scroll_y = ttk.Scrollbar(tree_frame,command=self.word_database.yview)
        scroll_y.pack(side=RIGHT, fill='y')

        self.word_database.configure(yscrollcommand = scroll_y.set, xscrollcommand = scroll_x.set)
        
        # Configure and position grid for TreeView
        self.word_database.grid_rowconfigure(0, weight = 1)
        self.word_database.grid_columnconfigure(0, weight = 1)

        # Assigning the heading names to the respective columns
        self.word_database.heading("#0", text="", anchor=CENTER)
        self.word_database.heading("ID", text="ID", anchor=NW)
        self.word_database.heading("Word", text="Keyword", anchor=NW)
        self.word_database.heading("Meaning", text="Description", anchor=NW)

        # Format the columns - Assign the width to respective columns
        self.word_database.column("#0", width=0, stretch=NO)
        self.word_database.column('ID', stretch=NO, minwidth=20, width=40,anchor=NW)
        self.word_database.column("Word", stretch=YES, width=100, minwidth=80,anchor=NW)
        self.word_database.column("Meaning", stretch=YES, width=500, minwidth=1150,anchor=NW)
        
        # Create Striped Row Tags
        self.word_database.tag_configure('oddrow', background="white")
        self.word_database.tag_configure('evenrow', background="lightblue")

        self.word_database.bind("<Double-1>", self.displaySelectedItemOnDoubleClick)
        self.ws_ent.bind("<Return>",self.searchData)

        # Calling pack method w.r.to treeview
        self.word_database.pack(side="left", fill=BOTH, expand=TRUE)

        # ====================== BUTTONS WIDGET===================================
        # Add Button
        add_button = Button(title_frame, text="Add Data", command=self.addData,
                            font=('Helvetica', 10, 'bold'), height=2, width=13, bd=4)
        add_button.grid(row=0, column=2, padx=2, pady=2, sticky="nsew")

        # Delete Button
        del_button = Button(title_frame, text="Delete Data",
                            font=('Helvetica', 10, 'bold'), height=2, width=13,
                            bd=4, command=self.deleteMultipleRecords)
        del_button.grid(row=1, column=2, padx=2, pady=2, sticky="nsew")

        # Update Button
        updt_button = Button(title_frame, text="Update Data",
                             font=('Helvetica', 10, 'bold'), height=2, width=13,
                             bd=4, command=self.updateData)
        updt_button.grid(row=1, column=3, padx=2, pady=2, sticky="nsew")

        #Clear Entry Boxes
        clear_record_button = Button(title_frame, text="Clear Entry Boxes", 
                                    font=('Helvetica', 10, 'bold'), height=2, width=16,
                                    bd=4, command=self.clearData)
        clear_record_button.grid(row=0, column=3, padx=2, pady=2, sticky="nsew")

        # Reset Button
        reset_button = Button(label_frame, text="Reset View",
                               font=('Helvetica', 10, 'bold'), height=2,
                               width=13, bd=4, command=self.resetView)
        reset_button.grid(row=0, column=2, padx=2, pady=2, sticky="nsew")

    # ======================FUNCTION DECLARATION===============================
    def importcsv(self):
        """Read CSV file from remote path.

        Args:
            filename(str): filename to read.
        Returns:
           
        Raises:
            
        """
        file_path=filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(("CSV File", "*.csv"),("All Files", "*.*")))
        # Check if user has selected a file
        if not file_path:
            return

        try:    
            with open(file_path, mode ='r', newline='', encoding='utf-8') as myFile:
                csvread = csv.reader(myFile, delimiter=',', skipinitialspace=True)
                   
                if not csvread:
                    raise ValueError('No data available to read')
                for entry in csvread:                  
                    if entry[0] =="" and entry[1] == "":
                        continue

                    self.dbms_inst.insert(entry[0], entry[1])
        except IOError:
            logging.error('', exc_info=True)

        self.populateView()

    def exportcsv(self):
        try:
            # Open the 'save CSV file' dialog
            file_path = filedialog.asksaveasfilename(initialdir=os.getcwd, title="Save CSV", defaultextension='.csv',filetypes=(("CSV File", "*.csv"),("All Files", "*.*")))

            # Check if user has selected a file
            if not file_path:
                return

            try:    
                with open (file_path,mode='w', newline='', encoding='utf-8') as myFile:
                    exp_writer=csv.writer(myFile, delimiter=',', skipinitialspace=True)

                    if not exp_writer:
                        raise ValueError('No data available to export')
                    
                    for record  in self.dbms_inst.fetch(''):
                        if record[1] =="" and record[2] == "":
                            continue                   
                        exp_writer.writerow((record[1].strip(),record[2].strip()))

            except IOError:
                logging.error('', exc_info=True)
            finally:
                messagebox.showinfo("Data Exported", "Your Data has been exported to " + os.path.basename(file_path) + " successfully")
        
        except FileNotFoundError:
            return "cancelled"

    def populateView(self, word=''):
        # Clear the Treeview
        self.word_database.delete(*self.word_database.get_children())

        # Add our data to the screen
        global count
        count = 0
        for record  in self.dbms_inst.fetch(word):
            #print(record )  # print all records in the database

            # Add Data in the TreeView
            if count % 2 == 0:
                self.word_database.insert(parent='', index='end',iid=count, text="", 
                                          values=(record[0], record[1],record[2]),tags=('evenrow',))
            else:
                self.word_database.insert(parent='', index='end',iid=count, text="",
                                          values=(record[0], record[1],record[2]),tags=('oddrow',))
            # increment counter
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
            #Add logic for message box
            if result == 1:  # True if OK button is clicked
                selected_rowid = self.word_database.selection()
                # Create List of ID's
                ids_to_delete = []
                # Add selections to ids_to_delete list
                for record in selected_rowid:
                    #ids_to_delete.append(tuple([int(record[1:], 16)]))
                    ids_to_delete.append(self.word_database.item(record,'values')[0])
                
                self.dbms_inst.remove_many(ids_to_delete)
                
                # Delete From Treeview
                for record in selected_rowid:
                    self.word_database.delete(record)

        except Exception:
            messagebox.showinfo("Message", traceback.print_exc())
        finally:
            #self.populateView()
            self.clearData()

    def clearData(self):
        self.entWordToAdd.delete(0, END)
        self.entDescription.delete(0, END)

    def resetView(self):
        self.ws_ent.delete(0, END)
        self.populateView()

    def searchData(self,event):
        # Add our data to the screen
        global count
        count = 0

        # Clear the Treeview
        self.word_database.delete(*self.word_database.get_children())

        for record  in self.dbms_inst.fetch(self.ws_ent.get()):
            # Add Data in the TreeView
            if count % 2 == 0:
                self.word_database.insert(parent='', index='end',iid=count, text="", 
                                        values=(record[0], record[1],record[2]),tags=('evenrow',))
            else:
                self.word_database.insert(parent='', index='end',iid=count, text="",
                                        values=(record[0], record[1],record[2]),tags=('oddrow',))
            # increment counter
            count += 1

    # create a function to display the selected row from treeview on double click
    def displaySelectedItemOnDoubleClick(self,event):
        # clear entries
        self.clearData()

        try:
            global item
            # Grab Record Number
            item =self.word_database.identify('item',event.x,event.y)
            '''print(item)
            print('********** tree mouse click event **********')
            print('clicked on', self.word_database.item(item)['values'])
            print('event.x: %d, event.y: %d' % (event.x, event.y))
            print(self.word_database.item(self.word_database.selection())['values'])
            print('******************************************\n') '''

        except Exception as e:
            messagebox.showinfo("Message", traceback.print_exc(e))
        finally:
            # Grab Record Values
            values = self.word_database.item(self.word_database.selection(), 'values')
            # Output to Entry Boxes
            self.entWordToAdd.insert(0, self.word_database.item(item)['values'][1])
            self.entDescription.insert(0, self.word_database.item(item)['values'][2])

    def updateData(self):
        try:
            self.dbms_inst.update(self.word_database.item(item)['values'][0],self.entWordToAdd.get(), self.entDescription.get())
        except Exception as e:
            messagebox.showinfo("Message", traceback.print_exc(e))
        finally:
            self.populateView()

    def Exit_App(self):
        # result = messagebox.askokcancel("Quit", "Are you sure you want to exit?", icon="warning")
        # if result > 0:
        self.root.destroy()
        exit()


if __name__ == '__main__':
    window = Tk()
    # Creating object of photoimage class
    # Image should be in the same folder
    # in which script is saved
    p1 = PhotoImage(file = 'icon.png')

    # Setting icon of master window
    window.iconphoto(False, p1)
    
    window.wm_attributes('-fullscreen', 'false')
    application = ConfigureGUI(window)
    application.populateView()
    window.protocol('WM_DELETE_WINDOW', application.Exit_App)
    window.mainloop()
