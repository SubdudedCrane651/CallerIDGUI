from tkinter import ttk

import tkinter as tk

import sqlite3

def View():

    con1 = sqlite3.connect("CallerID.db")

    cur1 = con1.cursor()

    cur1.execute("SELECT * FROM phonecalls ORDER BY ID DESC")

    rows = cur1.fetchall()    

    for row in rows:

        #print(row) 

        tree.insert("", tk.END, values=row)        

    con1.close()


# connect to the database

root = tk.Tk()

root.title("Calls Received")

tree = ttk.Treeview(root, column=("c1", "c2", "c3", "c4"), show='headings')

tree.column("#1", anchor=tk.CENTER)

tree.heading("#1", text="ID")

tree.column("#2", anchor=tk.CENTER)

tree.heading("#2", text="NAME")

tree.column("#3", anchor=tk.CENTER)

tree.heading("#3", text="PHONENUMBER")

tree.column("#4", anchor=tk.CENTER)

tree.heading("#4", text="DATE")

tree.pack()

button1 = tk.Button(text="Display data", command=View)

button1.pack(pady=10)

root.mainloop()