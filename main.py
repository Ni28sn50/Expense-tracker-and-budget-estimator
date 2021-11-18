
# monthly expense and budget estimator.

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3


def firstwin():
    global font1, font2, uname
    win1 = Tk()
    win1.title("Log in")
    win1.geometry('1000x600')
    win1.maxsize(1000, 600)
    win1.minsize(1000, 600)

    font1 = ("Times", 25, "bold")
    font2 = ("Roboto Mono", 18)

    f1 = Frame(win1, height=600, width=1000, bg="Black")
    f1.propagate(0)
    f1.place(x=0, y=0)

    uname = StringVar()
    password = StringVar()

    l0 = Label(f1, text="Monthly/Daily Expenses Tracker", font=font1, bg="Black", fg="White")
    l0.place(x=295, y=45)
    l01 = Label(f1, text="Sign in", font=("Times", 20, "bold"), bg="Black", fg="White")
    l01.place(x=470, y=130)
    l1 = Label(f1, text='User Name:', font=font2, bg="Black", fg="White")
    l1.place(x=250, y=210)
    e1 = Entry(f1, textvariable=uname, width=50, border=2)
    e1.place(x=450, y=215)

    l2 = Label(f1, text='Password:', font=font2,  bg="Black", fg="White")
    l2.place(x=250, y=290)
    e2 = Entry(f1, textvariable=password, show = '*', width=50, border=2)
    e2.place(x=450, y=295)
    login_but = Image.open("images/login.png")
    login_but = login_but.resize((100,40))
    login_but = ImageTk.PhotoImage(login_but)

    reset_but = Image.open("images/reset.png")
    reset_but = reset_but.resize((100,40))
    reset_but = ImageTk.PhotoImage(reset_but)

    Button(f1, text="Login", cursor="hand2", command=lambda: login(uname.get(), password.get()), image=login_but, bg="black", borderwidth=0, highlightthickness=0).place(x=425, y=380)
    Button(f1, text="Reset", cursor="hand2", command=lambda: clear(uname, password),image=reset_but , bg="black", borderwidth=0, highlightthickness=0).place(x=575, y=380)
    Button(f1, text="Don't have an account?", cursor="hand2", command=create_account, fg='#89CFF0', bg="black", borderwidth=0, highlightthickness=0, font=font2+('underline',)).place(x=420, y=460)
    cvar = IntVar()
    cvar.set(2)
    win1.mainloop()


def clear(var1, var2):
    var1.set("")
    var2.set("")

def create_account():
    win3 = Toplevel()
    win3.title("Create account")
    win3.geometry('1000x600')
    win3.maxsize(750, 600)
    win3.minsize(750, 600)
    f4 = Frame(win3, height=600, width=750, bg="Black")
    f4.propagate(0)
    f4.place(x=0, y=0)
    name = StringVar()
    pswd = StringVar()
    con_pswd = StringVar()
    h_label = Label(f4, text="Enter account details", font=("Times", 20, "bold"), bg="Black", fg="White")
    h_label.place(x=250, y=45)
    n_label = Label(f4, text='User Name:', font=font2, bg="Black", fg="White")
    n_label.place(x=100, y=120)
    name_e = Entry(f4, textvariable=name, width=50, border=2)
    name_e.place(x=330, y=125)
    pswd_label = Label(f4, text='Password:', font=font2, bg="Black", fg="White")
    pswd_label.place(x=100, y=200)
    pswd_e = Entry(f4, textvariable=pswd, show='*', width=50, border=2)
    pswd_e.place(x=330, y=205)
    conpswd_label = Label(f4, text='Confirm Password:', font=font2, bg="Black", fg="White")
    conpswd_label.place(x=100, y=280)
    conpswd_e = Entry(f4, textvariable=con_pswd, show='*',  width=50, border=2)
    conpswd_e.place(x=330, y=285)
    Button(f4, cursor="hand2", command=lambda: chk_account(name.get(), pswd.get(), con_pswd.get()), text="Create account", fg='white', bg='#3895D3', border=4, font=("Roboto Mono", 14)).place(x=340, y=380)
    win3.mainloop()

def chk_account(name, pswd, con_pswd):
    if (len(name) == 0) or (len(pswd)==0):
        messagebox.showerror("Empty Field(s)", "None of the fields can be left empty!")
    elif pswd != con_pswd:
        messagebox.showerror("Error in passwords", "Entered password and Confirmation password are different!")
    else:
        list_of_names = cur.execute("SELECT * FROM Login WHERE name = ?", (name,)).fetchall()
        if len(list_of_names) == 0:
            messagebox.showinfo("Accout Creation Successful", "Account has been successfully created. Now you may close the Account Creation window.")
            cur.execute("INSERT INTO Login(name, password) VALUES(?, ?)", (name, pswd))
            conn.commit()
        else:
            messagebox.showerror("User Name already taken", "This User Name had already been taken, please try with a different User Name.")

def delall():
    for widgets in f3.winfo_children():
        widgets.destroy()

def chk_cost(cost):
    try:
        cost = float(cost)
    except:
        cost = -1
    return cost

def chk_rec(item, cost):
    if (len(item)) == 0 or (len(cost)) == 0:
        messagebox.showerror("Empty Field(s)", "Please enter details in all the fields.")
    else:
        cost = chk_cost(cost)
        if cost < 0:
            messagebox.showerror("Invalid Value", "Please enter valid value of Cost.")
        else:
            chk = cur.execute("SELECT EXISTS(SELECT * FROM Items WHERE item=?)", (item.upper(),)).fetchall()
            if chk[0][0] == 0:
                cur.execute("INSERT INTO Items(item) VALUES(?)", (item.upper(),))

            item_id = cur.execute("SELECT id FROM Items WHERE item=?", (item.upper(),)).fetchall()
            mon_spent = cur.execute("SELECT moneyspent FROM MonthlyExp WHERE user_id=? AND item_id=?", (user_id[0][0],item_id[0][0])).fetchall()
            if (len(mon_spent)>0):
                cur.execute("UPDATE MonthlyExp SET moneyspent=? WHERE user_id=? AND item_id=?", (sum(mon_spent[0]+(cost,)), user_id[0][0], item_id[0][0]))
            else:
                cur.execute("INSERT INTO MonthlyExp(user_id, item_id, moneyspent) VALUES(?, ?, ?)", (user_id[0][0], item_id[0][0], cost))
            messagebox.showinfo("Insertion Successful", "Record has been added successfully!")
            conn.commit()

def addrec(addrec_button):
    delall()
    item_name = StringVar()
    cost = StringVar()
    addrec_button['state'] = DISABLED
    for i in (btn_set - {addrec_button}):
        i['state'] = NORMAL
    h1_label = Label(f3, text="Enter details about Expenditure", font=("Times", 20, "bold"), bg="Black", fg="White")
    h1_label.place(x=150, y=25)
    itm_label = Label(f3, text="Item Name:", font=font2, bg="Black", fg="White")
    itm_label.place(x=100, y=125)
    itm_e = Entry(f3, textvariable=item_name, width=50, border=2)
    itm_e.place(x=300, y=130)
    cost_label = Label(f3, text="Cost:            Rs.", font=font2, bg="Black", fg="White")
    cost_label.place(x=100, y=205)
    cost_e = Entry(f3, textvariable=cost, width=50, border=2)
    cost_e.place(x=300, y=210)
    Button(f3, cursor="hand2", command=lambda: chk_rec(item_name.get(), cost.get()), text="Add Record", fg='white', bg='#3895D3', border=4, font=("Roboto Mono", 14)).place(x=260, y=320)
    Button(f3, cursor="hand2", command=lambda: clear(item_name, cost), text="Reset", fg='white', bg='#3895D3', border=4, width=10, font=("Roboto Mono", 14)).place(x=420, y=320)

def showall(showall_button):
    delall()
    showall_button['state'] = DISABLED
    for i in (btn_set - {showall_button}):
        i['state'] = NORMAL
    chk = cur.execute("SELECT EXISTS(SELECT * FROM MonthlyExp WHERE user_id=?)", (user_id[0][0],)).fetchall()
    if (chk[0][0]==0):
        norec_label = Label(f3, text="No records are present!", font=font1, bg="Black", fg="White")
        norec_label.pack(pady=60)
    else:
        table = cur.execute("SELECT Items.item, MonthlyExp.moneyspent FROM Items JOIN MonthlyExp ON Items.id=MonthlyExp.item_id WHERE MonthlyExp.user_id=?", (user_id[0][0],)).fetchall()
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
        style.map('Treeview', background=[('selected', 'blue')])
        tree = ttk.Treeview(f3, column=("Expenses", "Money Spent (Rs.)"), show='headings')
        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="Expenses")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="Money Spent (Rs.)")
        tree.tag_configure('oddrow', background="white")
        tree.tag_configure('evenrow', background="light blue")
        count = 0
        for rows in table:
            if count%2==0:
                tree.insert('', 'end', text="1", values=rows, tags=('evenrow',))
            else:
                tree.insert('', 'end', text="1", values=rows, tags=('oddrow',))
            count+=1
        tree.place(x=140, y=50)
        inst_label = Label(f3, text="(If number of items are more than 10, then you can either scroll down on the table or\nselect last row and press down key to view remaining items.)", bg='black', fg='white', font=("Arial", 12))
        inst_label.place(x=60, y=350)
        sum_exp = cur.execute('SELECT SUM(moneyspent) FROM MonthlyExp WHERE user_id=?', (user_id[0][0],)).fetchall()
        sum_label = Label(f3, text=f"Total Money Spent: Rs. {sum_exp[0][0]}", font=("Times", 20, "bold"), bg="Black", fg="White")
        sum_label.pack(side=BOTTOM, pady=100)

def edit(item_name, updt_item_name, updt_cost):
    if (len(item_name)==0):
        messagebox.showerror("No Item Name given", "You left the field in which you have to enter item name whose details are to be updated!")
    else:
        item_id = cur.execute("SELECT id FROM Items WHERE item=?", (item_name.upper(),)).fetchall()
        if (len(item_id) < 1):
            messagebox.showerror("Error", "The entered item is not present in the record.")
        else:
            chk = cur.execute("SELECT EXISTS(SELECT * FROM MonthlyExp WHERE user_id=? AND item_id=?)", (user_id[0][0], item_id[0][0],)).fetchall()
            if (chk[0][0]==0):
                messagebox.showerror("Error", "The entered item is not present in the record.")
            else:
                if (len(updt_item_name) == 0) and (len(updt_cost) == 0):
                    messagebox.showerror("Empty Fields", "Please fill at least one field among Updated Item name and Updated Cost.")

                elif len(updt_item_name)==0:
                    updt_cost = chk_cost(updt_cost)
                    if updt_cost < 0:
                        messagebox.showerror("Invalid value of Updated Cost", "Please enter valid value of Updated Cost.")
                    else:
                        cur.execute("UPDATE MonthlyExp SET moneyspent=? WHERE user_id=? AND item_id=?", (updt_cost, user_id[0][0], item_id[0][0]))
                        messagebox.showinfo("Updation Successful", "Record has been updated successfully!")

                elif len(updt_cost)==0:
                    item_id2 = cur.execute("SELECT id FROM Items WHERE item=?", (updt_item_name.upper(),)).fetchall()
                    if (len(item_id2)<1):
                        cur.execute("INSERT INTO Items(item) VALUES(?)", (updt_item_name.upper(),))
                        item_id2 = cur.execute("SELECT id FROM Items WHERE item=?", (updt_item_name.upper(),)).fetchall()
                        cur.execute("UPDATE MonthlyExp SET item_id=? WHERE user_id=? AND item_id=?", (item_id2[0][0], user_id[0][0], item_id[0][0]))
                    else:
                        chk2 = cur.execute("SELECT EXISTS(SELECT * FROM MonthlyExp WHERE user_id=? AND item_id=?)", (user_id[0][0], item_id2[0][0])).fetchall()
                        if (chk2[0][0]==0):
                            cur.execute("UPDATE MonthlyExp SET item_id=? WHERE user_id=? AND item_id=?", (item_id2[0][0], user_id[0][0], item_id[0][0]))
                        else:
                            cost1 = cur.execute("SELECT moneyspent FROM MonthlyExp WHERE user_id=? AND item_id=?", (user_id[0][0], item_id[0][0])).fetchall()
                            cost2 = cur.execute("SELECT moneyspent FROM MonthlyExp WHERE user_id=? AND item_id=?", (user_id[0][0], item_id2[0][0])).fetchall()
                            cur.execute("UPDATE MonthlyExp SET moneyspent=? WHERE user_id=? AND item_id=?", (sum(cost1[0]+cost2[0]), user_id[0][0], item_id2[0][0]))
                            cur.execute("DELETE FROM MonthlyExp WHERE user_id=? AND item_id=?", (user_id[0][0], item_id[0][0]))
                    messagebox.showinfo("Updation Successful", "Record has been updated successfully!")

                elif (len(updt_item_name) != 0) and (len(updt_cost) != 0):
                    item_id2 = cur.execute("SELECT id FROM Items WHERE item=?", (updt_item_name.upper(),)).fetchall()
                    updt_cost = chk_cost(updt_cost)
                    if updt_cost < 0:
                        messagebox.showerror("Invalid value of Updated Cost", "Please enter valid value of Updated Cost.")
                    else:
                        if (len(item_id2)<1):
                            cur.execute("INSERT INTO Items(item) VALUES(?)", (updt_item_name.upper(),))
                            item_id2 = cur.execute("SELECT id FROM Items WHERE item=?", (updt_item_name.upper(),)).fetchall()
                            cur.execute("UPDATE MonthlyExp SET item_id=?, moneyspent=? WHERE user_id=? AND item_id=?", (item_id2[0][0], updt_cost, user_id[0][0], item_id[0][0]))
                        else:
                            chk2 = cur.execute("SELECT EXISTS(SELECT * FROM MonthlyExp WHERE user_id=? AND item_id=?)", (user_id[0][0], item_id2[0][0])).fetchall()
                            if (chk2[0][0]==0):
                                cur.execute("UPDATE MonthlyExp SET item_id=?, moneyspent=? WHERE user_id=? AND item_id=?", (item_id2[0][0], updt_cost, user_id[0][0], item_id[0][0]))
                            else:
                                cost2 = cur.execute("SELECT moneyspent FROM MonthlyExp WHERE user_id=? AND item_id=?", (user_id[0][0], item_id2[0][0])).fetchall()
                                cur.execute("UPDATE MonthlyExp SET moneyspent=? WHERE user_id=? AND item_id=?", (sum(cost2[0]+(updt_cost,)), user_id[0][0], item_id2[0][0]))
                                cur.execute("DELETE FROM MonthlyExp WHERE user_id=? AND item_id=?", (user_id[0][0], item_id[0][0]))
                    messagebox.showinfo("Updation Successful", "Record has been updated successfully!")
            conn.commit()

def editrec(editrec_button):
    delall()
    editrec_button['state'] = DISABLED
    for i in (btn_set - {editrec_button}):
        i['state'] = NORMAL
    item_name = StringVar()
    updt_item_name = StringVar()
    updt_cost = StringVar()
    edit_label = Label(f3, text="Enter Item name whose details you want to edit:-", font=("Times", 20), bg="Black", fg="White")
    edit_label.place(x=65, y=25)
    item_label = Label(f3, text="Item Name:", font=("Times", 18), bg="Black", fg="White")
    item_label.place(x=65, y=100)
    itm_e = Entry(f3, textvariable=item_name, width=50, border=2)
    itm_e.place(x=305, y=105)
    edit_label2 = Label(f3, text="Enter updated details:-", font=("Times", 20), bg="Black", fg="White")
    edit_label2.place(x=65, y=175)
    inst_label = Label(f3, text="(Leave that field empty in which you don't want any updation)", font=("Times", 18), bg="Black", fg="White")
    inst_label.place(x=65, y=215)
    updt_item_label = Label(f3, text="Updated Item name:", font=("Times", 18), bg="Black", fg="White")
    updt_item_label.place(x=65, y=290)
    updt_item_e = Entry(f3, textvariable=updt_item_name, width=50, border=2)
    updt_item_e.place(x=305, y=295)
    cost_label = Label(f3, text="Updated Cost:       Rs.", font=("Times", 18), bg="Black", fg="White")
    cost_label.place(x=65, y=375)
    cost_e = Entry(f3, textvariable=updt_cost, width=50, border=2)
    cost_e.place(x=305, y=380)
    Button(f3, cursor="hand2", command=lambda: edit(item_name.get(), updt_item_name.get(), updt_cost.get()), text="Confirm Changes", fg='white', bg='#3895D3', border=4, font=("Roboto Mono", 14)).place(x=100, y=480)
    Button(f3, cursor="hand2", command=lambda: clear(updt_item_name, updt_cost), text="Reset values in Updated fields", fg='white', bg='#3895D3', border=4, font=("Roboto Mono", 14)).place(x=350, y=480)

def confirmdelrec(delitem):
    item_id = cur.execute("SELECT id FROM Items WHERE item=?", (delitem.upper(),)).fetchall()
    if (len(item_id)==0):
        messagebox.showerror("Error in Deletion", "The entered item is already not present in the record!")
    else:
        chk = cur.execute("SELECT EXISTS(SELECT * FROM MonthlyExp WHERE user_id=? AND item_id=?)", (user_id[0][0], item_id[0][0])).fetchall()
        if (chk[0][0]==0):
            messagebox.showerror("Error in Deletion", "The entered item is already not present in the record!")
        else:
            res = messagebox.askquestion("Confirm Deletion", "The record of the entered item will be deleted permanently from the record. Do you wish to continue?")
            if res=='yes':
                cur.execute("DELETE FROM MonthlyExp WHERE user_id=? AND item_id=?", (user_id[0][0], item_id[0][0]))
                messagebox.showinfo("Deletion Successful",  "The record of entered item has been deleted successfully!")
                conn.commit()
            else:
                pass

def delrec(delrec_button):
    delall()
    delrec_button['state'] = DISABLED
    for i in (btn_set - {delrec_button}):
        i['state'] = NORMAL
    delitem_name = StringVar()
    del_heading = Label(f3, text="Enter Item name whose details you want to delete:-", font=("Times", 20), bg="Black", fg="White")
    del_heading.place(x=65, y=50)
    delitem_label = Label(f3, text="Item Name:", font=("Times", 18), bg="Black", fg="White")
    delitem_label.place(x=65, y=150)
    delitm_e = Entry(f3, textvariable=delitem_name, width=50, border=2)
    delitm_e.place(x=305, y=155)
    Button(f3, cursor="hand2", command=lambda: confirmdelrec(delitem_name.get()), text="Confirm Deletion", fg='white', bg='#3895D3', border=4, font=("Roboto Mono", 14)).place(x=250, y=250)

def confirmdelall(password):
    chk = cur.execute("SELECT EXISTS(SELECT * FROM Login WHERE id=? AND password=?)", (user_id[0][0], password)).fetchall()
    if chk[0][0] == 0:
        messagebox.showerror("Wrong Password", "The entered password is wrong, deletion failed!")
    else:
        chk2 = cur.execute("SELECT EXISTS(SELECT * FROM MonthlyExp WHERE user_id=?)", (user_id[0][0],)).fetchall()
        if (chk2[0][0]==0):
            messagebox.showinfo("Deletion not required", "No records are present!")
        else:
            cur.execute("DELETE FROM MonthlyExp WHERE user_id=?", (user_id[0][0],))
            messagebox.showinfo("Deletion Successful", "All the records have been deleted successfully!")
            conn.commit()

def delallrec(delallrec_button):
    delall()
    delallrec_button['state'] = DISABLED
    for i in (btn_set - {delallrec_button}):
        i['state'] = NORMAL
    password = StringVar()
    warn_label = Label(f3, text="WARNING: You are about to delete all of your records.\nIf you wish to continue, then please enter your password.", font=("Times", 20), bg="Black", fg="White")
    warn_label.place(x=25, y=50)
    password_label = Label(f3, text="Enter Password:", font=("Times", 18), bg="Black", fg="White")
    password_label.place(x=65, y=170)
    password_e = Entry(f3, textvariable=password, show='*', width=50, border=2)
    password_e.place(x=305, y=175)
    Button(f3, cursor="hand2", command=lambda: confirmdelall(password.get()), text="Confirm Deletion", fg='white', bg='#3895D3', border=4, font=("Roboto Mono", 14)).place(x=250, y=250)

def login(uname, password):
    if (len(uname)==0) or (len(password)==0):
        messagebox.showerror("Error", "Please enter details in all the fields.")
    else:
        list_of_logrec = cur.execute("SELECT * FROM Login WHERE name=? AND password=?", (uname, password)).fetchall()
        if len(list_of_logrec) == 0:
            messagebox.showerror("Login error", "Please enter correct Login credentials.")
        else:
            global user_id
            user_id = cur.execute("SELECT id FROM Login WHERE name=?", (uname,)).fetchall()
            secwin()

def secwin():
    global f3, btn_set
    win2 = Toplevel()
    win2.title("Menu")
    win2.geometry('1000x600')
    win2.maxsize(1000, 600)
    win2.minsize(1000, 600)
    f2 = Frame(win2, height=600, width=300, borderwidth = 5, relief = SUNKEN, bg="#FFFAFA")
    f2.propagate(0)
    f2.place(x=0, y=0)
    l4 = Label(f2, text="Menu", font=font1, bg="#FFFAFA")
    l4.place(x=100, y=0)
    btn_set = set()
    addrec_button = Button(f2, text="Add a record", cursor="hand2", command=lambda: addrec(addrec_button), border=4, width=37, height=3)
    addrec_button.place(x=10, y=60)
    btn_set.add(addrec_button)
    showall_button = Button(f2, text="Show all records and Total Money Spent", cursor="hand2", command=lambda: showall(showall_button), border=4, width=37, height = 3)
    showall_button.place(x=10, y=160)
    btn_set.add(showall_button)
    editrec_button = Button(f2, text="Edit a record", cursor="hand2", command=lambda: editrec(editrec_button), border=4, width=37, height = 3)
    editrec_button.place(x=10, y=260)
    btn_set.add(editrec_button)
    delrec_button = Button(f2, text="Delete a record", cursor="hand2", command=lambda: delrec(delrec_button), border=4, width=37, height = 3)
    delrec_button.place(x=10, y=360)
    btn_set.add(delrec_button)
    delallrec_button = Button(f2, text="Delete all records", cursor="hand2", command=lambda: delallrec(delallrec_button), border=4, width=37, height = 3)
    delallrec_button.place(x=10, y=460)
    btn_set.add(delallrec_button)
    f3 = Frame(win2, height=600, width=700, borderwidth = 5, relief = SUNKEN, bg="Black")
    f3.propagate(0)
    f3.place(x=300, y=0)
    inst = "Please select the desired option from the Menu."
    l5 = Label(f3, text=inst, font=font2, fg="White", bg="Black")
    l5.place(x=80, y=0)

conn = sqlite3.connect('dbmonthexp.sqlite')
cur = conn.cursor()
lst = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Login';").fetchall()
if lst == []:
    cur.executescript('''CREATE TABLE Login(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT UNIQUE, password TEXT);
                         CREATE TABLE Items(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, item TEXT UNIQUE);
                         CREATE TABLE MonthlyExp(user_id INTEGER, item_id INTEGER, moneyspent DECIMAL(10,2));''')
firstwin()
