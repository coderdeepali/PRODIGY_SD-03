from tkinter import *
import mysql.connector
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

root = Tk()
root.title("Contact List")
width = 1000
height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="#0099cc")

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password ',
    'database': 'database_name',
}

FIRSTNAME = StringVar()
LASTNAME = StringVar()
GENDER = StringVar()
AGE = StringVar()
EMAIL = StringVar()
CONTACT = StringVar()
mem_id = None

def Database():
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS member (mem_id INT AUTO_INCREMENT PRIMARY KEY, firstname VARCHAR(255), lastname VARCHAR(255), gender VARCHAR(10), age INT, email TEXT, contact VARCHAR(15))")
    cursor.execute("SELECT * FROM member ORDER BY lastname ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()
def OnSelected(event):
    global mem_id
    curItem = tree.focus()
    contents = (tree.item(curItem))
    selecteditem = contents['values']
    mem_id = selecteditem[0]

    FIRSTNAME.set(selecteditem[1])
    LASTNAME.set(selecteditem[2])
    GENDER.set(selecteditem[3])
    AGE.set(selecteditem[4])
    EMAIL.set(selecteditem[5])
    CONTACT.set(selecteditem[6])
def SubmitData():
    if FIRSTNAME.get() == "" or LASTNAME.get() == "" or GENDER.get() == "" or AGE.get() == "" or EMAIL.get() == "" or CONTACT.get() == "":
        result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
    else:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO member (firstname, lastname, gender, age, address, contact) VALUES(%s, %s, %s, %s, %s, %s)",
                       (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), AGE.get(), EMAIL.get(), CONTACT.get()))
        conn.commit()
        cursor.execute("SELECT * FROM member ORDER BY lastname ASC")
        fetch = cursor.fetchall()
        tree.delete(*tree.get_children())
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        AGE.set("")
        EMAIL.set("")
        CONTACT.set("")

def UpdateData():
    if GENDER.get() == "":
        result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
    else:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("UPDATE member SET firstname = %s, lastname = %s, gender = %s, age = %s, address = %s, contact = %s WHERE mem_id = %s",
                       (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), AGE.get(), EMAIL.get(), CONTACT.get(), mem_id))
        conn.commit()
        cursor.execute("SELECT * FROM member ORDER BY lastname ASC")
        fetch = cursor.fetchall()
        tree.delete(*tree.get_children())
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        AGE.set("")
        EMAIL.set("")
        CONTACT.set("")

def DeleteData():
    if not tree.selection():
        result = tkMessageBox.showwarning('', 'Please Select Something First!', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            conn = mysql.connector.connect(**mysql_config)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM member WHERE mem_id = %s", (selecteditem[0],))
            conn.commit()
            cursor.close()
            conn.close()

def AddNewWindow():
    global NewWindow
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    AGE.set("")
    EMAIL.set("")
    CONTACT.set("")
    NewWindow = Toplevel()
    NewWindow.title("Contact List")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) - 455) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    NewWindow.resizable(0, 0)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))

    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
    Male = Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male", font=('arial', 14)).pack(side=LEFT)
    Female = Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female", font=('arial', 14)).pack(side=LEFT)

    lbl_title = Label(FormTitle, text="Adding New Contacts", font=('arial', 16), bg="#66ff66",  width=300)
    lbl_title.pack(fill=X)
    lbl_firstname = Label(ContactForm, text="Firstname", font=('arial', 14), bd=5)
    lbl_firstname.grid(row=0, sticky=W)
    lbl_lastname = Label(ContactForm, text="Lastname", font=('arial', 14), bd=5)
    lbl_lastname.grid(row=1, sticky=W)
    lbl_gender = Label(ContactForm, text="Gender", font=('arial', 14), bd=5)
    lbl_gender.grid(row=2, sticky=W)
    lbl_age = Label(ContactForm, text="Age", font=('arial', 14), bd=5)
    lbl_age.grid(row=3, sticky=W)
    lbl_email = Label(ContactForm, text="EMAIL", font=('arial', 14), bd=5)
    lbl_email.grid(row=4, sticky=W)
    lbl_contact = Label(ContactForm, text="Contact", font=('arial', 14), bd=5)
    lbl_contact.grid(row=5, sticky=W)

    firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14))
    firstname.grid(row=0, column=1)
    lastname = Entry(ContactForm, textvariable=LASTNAME, font=('arial', 14))
    lastname.grid(row=1, column=1)
    RadioGroup.grid(row=2, column=1)
    age = Entry(ContactForm, textvariable=AGE, font=('arial', 14))
    age.grid(row=3, column=1)
    email = Entry(ContactForm, textvariable=EMAIL, font=('arial', 14))
    email.grid(row=4, column=1)
    contact = Entry(ContactForm, textvariable=CONTACT, font=('arial', 14))
    contact.grid(row=5, column=1)

    btn_addcon = Button(ContactForm, text="Save", width=50, command=SubmitData)
    btn_addcon.grid(row=6, columnspan=2, pady=10)

def EditWindow():
    global EditWindow
    if not tree.selection():
        result = tkMessageBox.showwarning('', 'Please Select Something First!', icon="warning")
    else:
        EditWindow = Toplevel()
        EditWindow.title("Edit Contact")
        width = 400
        height = 300
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = ((screen_width/2) - 455) - (width/2)
        y = ((screen_height/2) + 20) - (height/2)
        EditWindow.resizable(0, 0)
        EditWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))

        FormTitle = Frame(EditWindow)
        FormTitle.pack(side=TOP)
        ContactForm = Frame(EditWindow)
        ContactForm.pack(side=TOP, pady=10)
        RadioGroup = Frame(ContactForm)
        Male = Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male", font=('arial', 14)).pack(side=LEFT)
        Female = Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female", font=('arial', 14)).pack(side=LEFT)

        lbl_title = Label(FormTitle, text="Edit Contact", font=('arial', 16), bg="#66ff66", width=300)
        lbl_title.pack(fill=X)
        lbl_firstname = Label(ContactForm, text="Firstname", font=('arial', 14), bd=5)
        lbl_firstname.grid(row=0, sticky=W)
        lbl_lastname = Label(ContactForm, text="Lastname", font=('arial', 14), bd=5)
        lbl_lastname.grid(row=1, sticky=W)
        lbl_gender = Label(ContactForm, text="Gender", font=('arial', 14), bd=5)
        lbl_gender.grid(row=2, sticky=W)
        lbl_age = Label(ContactForm, text="Age", font=('arial', 14), bd=5)
        lbl_age.grid(row=3, sticky=W)
        lbl_email = Label(ContactForm, text="Email", font=('arial', 14), bd=5)
        lbl_email.grid(row=4, sticky=W)
        lbl_contact = Label(ContactForm, text="Contact", font=('arial', 14), bd=5)
        lbl_contact.grid(row=5, sticky=W)

        firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14))
        firstname.grid(row=0, column=1)
        lastname = Entry(ContactForm, textvariable=LASTNAME, font=('arial', 14))
        lastname.grid(row=1, column=1)
        RadioGroup.grid(row=2, column=1)
        age = Entry(ContactForm, textvariable=AGE, font=('arial', 14))
        age.grid(row=3, column=1)
        address = Entry(ContactForm, textvariable=EMAIL, font=('arial', 14))
        address.grid(row=4, column=1)
        contact = Entry(ContactForm, textvariable=CONTACT, font=('arial', 14))
        contact.grid(row=5, column=1)

        curItem = tree.focus()
        contents = (tree.item(curItem))
        selecteditem = contents['values']
        mem_id = selecteditem[0]
        FIRSTNAME.set(selecteditem[1])
        LASTNAME.set(selecteditem[2])
        GENDER.set(selecteditem[3])
        AGE.set(selecteditem[4])
        EMAIL.set(selecteditem[5])
        CONTACT.set(selecteditem[6])

        btn_editcon = Button(ContactForm, text="Save", width=50, command=UpdateData)
        btn_editcon.grid(row=6, columnspan=2, pady=10)

Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP, padx=10, pady=10)
Mid = Frame(root, width=500, bg="#6666ff")
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=100)
MidLeft.pack(side=LEFT, padx=10, pady=10)
MidLeftPadding = Frame(Mid, width=370, bg="#6666ff")
MidLeftPadding.pack(side=LEFT)
MidRight = Frame(Mid, width=100)
MidRight.pack(side=RIGHT, padx=10, pady=10)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP, padx=10, pady=10)

title_font = ("Helvetica", 20, "bold")
btn_font = ("Helvetica", 12)

lbl_title = Label(Top, text="Contact Management System", font=('arial', 20, 'bold'), width=500, bg="#34495e", fg="white")
lbl_title.pack(fill=X,pady=10)

btn_edit = Button(MidRight, text="EDIT", bg="orange", fg="white", font=('arial', 14, 'bold'), command=EditWindow)
btn_edit.pack(side=RIGHT)

btn_add = Button(MidLeft, text="+ ADD NEW", bg="#27ae60", fg="white", font=('arial', 14, 'bold'), command=AddNewWindow)
btn_add.pack()
btn_delete = Button(MidRight, text="DELETE", bg="#e74c3c", fg="white", font=('arial', 14, 'bold'),command=DeleteData)
btn_delete.pack(side=RIGHT)

style = ttk.Style()
style.theme_use("clam")  
style.configure("Treeview",
                background="#ecf0f1",  
                fieldbackground="#ecf0f1",  
                )
style.map("Treeview", background=[("selected", "#ecf0f1")])

style = ttk.Style()
style.theme_use("clam")

# Increase font size for Treeview values
style.configure("Treeview.Treeview", font=('Arial', 16), rowheight=30)  
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("MemberID", "Firstname", "Lastname", "Gender", "Age", "Email", "Contact"), height=700, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
style.configure("Treeview.Treeview", font=('Arial', 16), rowheight=30)  
style = ttk.Style()
style.theme_use("clam")
style.map("Treeview", background=[("selected", "#3498db")])  
style.configure("Treeview.Heading", 
    font=('Arial', 14, 'bold'),
    background="#34495e",  
    foreground="white", 
    borderwidth=1, 
    relief="solid")  
style.configure("Treeview.Treeview",            
    borderwidth=1,
    relief="solid",  
)

tree.heading('MemberID', text="MemberID", anchor=W)
tree.heading('Firstname', text="Firstname", anchor=W)
tree.heading('Lastname', text="Lastname", anchor=W)
tree.heading('Gender', text="Gender", anchor=W)
tree.heading('Age', text="Age", anchor=W)
tree.heading('Email', text="Email", anchor=W)
tree.heading('Contact', text="Contact", anchor=W)

tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=120)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=90)
tree.column('#5', stretch=NO, minwidth=0, width=60)
tree.column('#6', stretch=NO, minwidth=0, width=150)
tree.column('#7', stretch=NO, minwidth=0, width=120)
tree.pack()
tree.bind('<Double-1>', OnSelected)

if __name__ == '__main__':
    Database()
    root.mainloop()
