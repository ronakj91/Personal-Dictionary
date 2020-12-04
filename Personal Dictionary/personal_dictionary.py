from tkinter import *
import dbms as db
from functools import partial
from tkinter import messagebox


window=Tk()
window.title("GUI DICTIONARY")

class Table: 
      
    def __init__(self,root, lst): 
        total_rows = len(lst) 
        total_columns = len(lst[0])
        root=Tk()
        root.title("Data")  
        # code for creating table 
        for i in range(total_rows): 
            for j in range(1,total_columns): 
                if j == 1:
                    self.e = Entry(root, fg='blue', font=('Arial',16,'bold'))
                else:
                    self.e = Entry(root, fg='blue', font=('Arial',16,'bold'), width=50) 
                  
                self.e.grid(row=i, column=j) 
                self.e.insert(END, lst[i][j]) 
                # self.e.command(readWord(self.e.get()))
        root.mainloop()
 

# initialize (connection established to the database)
dbms_inst = db.dbms("dictionary", "Dict_personal.db")

# create a new table
list = ["Word", "Meaning"]    

sql_create_table = dbms_inst.get_sql_for_creating_table(list)  

print(sql_create_table)
print()
dbms_inst.create_table(sql_create_table)

# insert data            
sql = dbms_inst.get_sql_for_creating_entry(list)            
print(sql)
print()

def mean():
    t.insert(END,"data")
    
def reset():
    word.set("")
    meaning.set("")
    t.delete(1.0,END)
    t1.delete(1.0,END)
    
def exit():
    window.destroy()
    
def addWord(t,t1):
    word_to_add = t.get()
    meaning = t1.get()
    
    try:
        entry = (word_to_add, meaning)
        cursor = dbms_inst.create_entry(sql, entry)
        msg = messagebox.showinfo( "Message", "Word added")
    except Exception:
        str = traceback.print_exc()
        msg = messagebox.showinfo( "Message", str)
        
    reset()
        
        
def showWords():
    word_list = dbms_inst.select_entries("SELECT * FROM dictionary")
    print(word_list)
    
    # take the data            
    lst = word_list
       
    # find total number of rows and 
    # columns in list
    
    ret = Table(window,lst) 
    
def readWord(word):
    print("Hello")
    print(word)
    
    



# Entry Box Label
b = Label(window, text="Enter Word")
b.config(font=(30))
b.grid(row=1,column=1)

# Entry Box
word_to_find = StringVar()
e = Entry(window, textvariable = word_to_find, width=20)
e.grid(row=1, column=2)

# Button
b1 = Button(window, text="Find!", bg="skyblue", width="10", command=showWords)
# b1.config(font=(20))
b1.grid(row=1,column=3)

# Text Box
word = StringVar()
t = Entry(window, textvariable = word, width = 30)
t.grid(row=2, column=1,  columnspan = 2)

meaning = StringVar()
t1 = Entry(window, textvariable = meaning, width = 60)
t1.grid(row=2, column=3,  columnspan = 4)

# Add Button
addWord = partial(addWord, t, t1)
add = Button(window, text="Add", bg="skyblue", width=10, command=addWord)
add.grid(row=1,column=4)


# Reset Button
r = Button(window, text="RESET", bg="skyblue", width=10, command=reset)
r.grid(row=1,column=5)

# Exit Button
ex = Button(window, text="EXIT", bg="skyblue", width=10, command=exit)
ex.grid(row=1,column=6)


window.mainloop()