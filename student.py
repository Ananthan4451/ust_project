from tkinter import *
import sqlite3
from tkinter import messagebox

class DB:
    def __init__(self):
        try:
            self.conn = sqlite3.connect("student.db")
            self.cur = self.conn.cursor()
            self.cur.execute(
                "CREATE TABLE IF NOT EXISTS student (id INTEGER PRIMARY KEY, name TEXT, branch TEXT, contact INTEGER, "
                "address TEXT)")
            self.conn.commit()
        except:
            messagebox.showinfo("Error", "Cannot connect to database")

    def __del__(self):
        self.conn.close()


    def view(self):
        self.cur.execute("SELECT * FROM student")
        rows = self.cur.fetchall()
        return rows

    def insert(self, name, branch, contact, address):
        self.cur.execute("INSERT INTO student VALUES (NULL,?,?,?,?)", (name, branch, contact, address))
        self.conn.commit()
        self.view()

    def update(self, id, name, branch, contact, address):
        self.cur.execute("UPDATE student SET name=?, branch=?, contact=?, address=? WHERE id=?",
                         (name, branch, contact, address, id))
        self.view()

    def delete(self, id):
        self.cur.execute("DELETE FROM student WHERE id=?", (id,))
        self.conn.commit()
        self.view()


db = DB()


def get_selected_row(event):
    global selected_tuple
    try:
        index = list1.curselection()[0]
        selected_tuple = list1.get(index)
        txtname.delete(0, END)
        txtname.insert(END, selected_tuple[1])
        txtbranch.delete(0, END)
        txtbranch.insert(END, selected_tuple[2])
        txtnumber.delete(0, END)
        txtnumber.insert(END, selected_tuple[3])
        txtaddress.delete(0, END)
        txtaddress.insert(END, selected_tuple[4])
    except:
        messagebox.showinfo("Error","please select a value")


def view_command():
    list1.delete(0, END)
    for row in db.view():
        list1.insert(END, row)
    txtname.delete(0, END)
    txtbranch.delete(0, END)
    txtnumber.delete(0, END)
    txtaddress.delete(0, END)


def add_command():
    if name_text.get() and branch_text.get() and number_text.get().isnumeric() == True and len(number_text.get()) == 10 and address_text.get():
        db.insert(name_text.get(), branch_text.get(), number_text.get(), address_text.get())
        list1.delete(0, END)
        list1.insert(END, (name_text.get(), branch_text.get(), number_text.get(), address_text.get()))
        list1.delete(0, END)
        messagebox.showinfo("Successful", "Data Inserted!")
        txtname.delete(0, END)
        txtbranch.delete(0, END)
        txtnumber.delete(0, END)
        txtaddress.delete(0, END)
    else:
        messagebox.showinfo("Error", "Fill all fields with correct values")



def delete_command():
    if name_text.get() and branch_text.get() and number_text.get() and address_text.get():
        db.delete(selected_tuple[0])
        messagebox.showinfo("Successful", "Data Deleted!")
        list1.delete(0, END)
        txtname.delete(0, END)
        txtbranch.delete(0, END)
        txtnumber.delete(0, END)
        txtaddress.delete(0, END)
    else:
        messagebox.showinfo("Error", "Please select a field")


def clear_command():
    list1.delete(0, END)
    txtname.delete(0, END)
    txtbranch.delete(0, END)
    txtnumber.delete(0, END)
    txtaddress.delete(0, END)


def update_command():
    try:
        if name_text.get() and branch_text.get() and number_text.get() and address_text.get():
            db.update(selected_tuple[0], name_text.get(), branch_text.get(), number_text.get(), address_text.get())
            messagebox.showinfo("Successful", "Data Updated!")
        else:
            messagebox.showinfo("Error", "Please select a data")
    except:
        messagebox.showinfo("Error", "Table not updated")
    list1.delete(0, END)
    txtname.delete(0, END)
    txtbranch.delete(0, END)
    txtnumber.delete(0, END)
    txtaddress.delete(0, END)


# ----------------GUI--------------------
root = Tk()
root.geometry("1100x500+0+0")
root.title("Student Management")


def on_closing():
    dd = db
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        del dd
root.protocol("WM_DELETE_WINDOW", on_closing)  # handle window closing

# heading
lblinfo = Label(root, font=('aria', 30, 'bold'), text="STUDENT MANAGEMENT", fg="black", bd=10)
lblinfo.place(x=330, y=30)

lblname = Label(root, font=('aria', 16, 'bold'), text="Name",  bd=10)
lblname.place(x=40, y=130)
name_text = StringVar()
txtname = Entry(root, font=('ariel', 16, 'bold'), bd=6, insertwidth=4,
                textvariable=name_text)
txtname.place(x=250, y=130)

lblbranch = Label(root, font=('aria', 16, 'bold'), text="Branch",  bd=10)
lblbranch.place(x=40, y=180)
branch_text = StringVar()
txtbranch = Entry(root, font=('ariel', 16, 'bold'), bd=6, insertwidth=4,
                  textvariable=branch_text)
txtbranch.place(x=250, y=180)

lblnumber = Label(root, font=('aria', 16, 'bold'), text="Contact Number", bd=10, anchor='w')
lblnumber.place(x=40, y=230)
number_text = StringVar()
txtnumber = Entry(root, font=('ariel', 16, 'bold'), bd=6, insertwidth=4,
                  textvariable=number_text)
txtnumber.place(x=250, y=230)

lbladdress = Label(root, font=('aria', 16, 'bold'), text="Place",  bd=10, anchor='w')
lbladdress.place(x=40, y=280)
address_text = StringVar()
txtaddress = Entry(root, font=('ariel', 16, 'bold'), bd=6, insertwidth=4,
                   textvariable=address_text)
txtaddress.place(x=250, y=280)

btninsert = Button(root, bd=8, fg="black", font=('ariel', 16, 'bold'), width=8, text="Insert",
                  command=add_command)
btninsert.place(x=70, y=350)

btnview = Button(root, bd=8, fg="black", font=('ariel', 16, 'bold'), width=8, text="View All",
                 command=view_command)
btnview.place(x=210, y=350)

btndelete = Button(root, bd=8, fg="black", font=('ariel', 16, 'bold'), width=8, text="Delete",
                 command=delete_command)
btndelete.place(x=350, y=350)

btnupdate = Button(root, bd=8, fg="black", font=('ariel', 16, 'bold'), width=8, text="Update",
                    command=update_command)
btnupdate.place(x=150, y=420)

btnclear = Button(root, bd=8, fg="black", font=('ariel', 16, 'bold'), width=8, text="Clear",
                 command=clear_command)
btnclear.place(x=300, y=420)

# list
list1 = Listbox(root, height=20, width=85)
list1.place(x=550, y=130)

sb1 = Scrollbar(root, orient="vertical")
sb1.place(x=1050, y=130)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.bind('<<ListboxSelect>>', get_selected_row)

root.mainloop()
