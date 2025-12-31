from tkinter import ttk

import tkinter as tk

import sqlite3

import json
import mysql.connector

def load_mysql_config(path="config.json"):
    with open(path, "r") as file:
        data = json.load(file)
        return data["mysql"]

def View():

        # Load MySQL config from JSON
        config = load_mysql_config()

        if config["host"] == "SQLite":
           SQLite=True
        else:
           SQLite=False   

        if SQLite:
    
          con = sqlite3.connect('CallerID.db')

          rows = con.execute("SELECT * FROM phonecalls ORDER BY ID DESC LIMIT 20")

        else:        

            # Connect to MySQL
            con1 = mysql.connector.connect(
                host=config["host"],
                user=config["user"],
                password=config["password"],
                database=config["database"],
                port=config.get("port", 3306)
            )

            cur1 = con1.cursor()
            cur1.execute("SELECT * FROM phonecalls ORDER BY ID DESC LIMIT 20")
            rows = cur1.fetchall()  

        for row in rows:

            tree.insert("", tk.END, values=row)

        if SQLite:
            con.close()
        else:
            con1.close()

# connect to the database

root = tk.Tk()

root.title("Calls Received")

tree = ttk.Treeview(root, column=("c1", "c2", "c3", "c4"), show='headings')

tree.column("#1", anchor=tk.CENTER)

tree.heading("#1", text="ID")

tree.column("#2", anchor=tk.CENTER)

config = load_mysql_config()

if config["host"] == "SQLite":
    SQLite=True
else:
    SQLite=False  

if SQLite:

    tree.heading("#2", text="NAME")

    tree.column("#3", anchor=tk.CENTER)

    tree.heading("#3", text="PHONENUMBER")

else:

    tree.heading("#2", text="PHONENUMBER")

    tree.column("#3", anchor=tk.CENTER)

    tree.heading("#3", text="NAME")

tree.column("#4", anchor=tk.CENTER)

tree.heading("#4", text="DATE")

tree.pack()

button1 = tk.Button(text="Display data", command=View)

button1.pack(pady=10)

root.mainloop()