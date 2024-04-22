# import tkinter as tk
# from tkinter import *
# import mysql.connector
# import os
# from tkinter import messagebox
# import subprocess
# from PIL import ImageTk, Image
# from tkinter import ttk

# # Create the main window
# window = tk.Tk()
# window.title("User Account")
# window.geometry('1200x680+300+200')
# window.resizable(False, False)
# window.configure(bg="#d3bbab")

# # Establish Connection
# connection = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Chetra1234",  # Change it to your password
#     database="Library"
# )

# # Create a cursor
# cursor = connection.cursor()

# # Function to populate the table view with data from the database
# def populate_table():
#     cursor.execute("SELECT id, full_name, email, username FROM user_account")
#     for row in cursor.fetchall():
#         table.insert("", "end", values=row)
# def search_product():
#     search_query = search_entry.get()
#     cursor.execute("SELECT id, full_name, email, username FROM user_account WHERE username LIKE %s OR id = %s", ('%' + search_query + '%', search_query))
#     # Clear the table before populating with search results
#     for item in table.get_children():
#         table.delete(item)
#     for row in cursor.fetchall():
#         table.insert("", "end", values=row)
# # Button Click Functions
# def bookmanage_click():
#     window.destroy()
#     subprocess.run(['python', 'admin_bookmanagement.py'])

# def Inventory_click():
#     window.destroy()
#     subprocess.run(['python', 'admin_inventory.py'])

# def userhis_click():
#     window.destroy()
#     subprocess.run(['python', 'admin_history.py'])

# def exit_click():
#     window.destroy()
#     subprocess.run(['python', 'login.py'])

# # Custom Font for Buttons
# button_font = ("Lato", 14)  # Custom font for buttons
# entry_font = ("Lato", 13)  # Custom font for entries

# # Frame for Buttons
# button_frame = tk.Frame(window, bg="#3d291f")
# button_frame.pack(side="top", fill="x", padx=0, pady=0)

# # Logo
# logo_image = Image.open("bookstack_logo.png")
# logo_image = logo_image.resize((50, 60))
# logo_image = ImageTk.PhotoImage(logo_image)
# logo_label = tk.Label(button_frame, image=logo_image, highlightthickness=0, bd=0, bg="#3d291f", compound=tk.LEFT)
# logo_label.pack(side="left", padx=0, pady=0, anchor="nw")

# # Buttons for Products, Customers, Manage, Exit
# bookManage_button = tk.Button(button_frame, text="Book Management", bg='#563d2d', fg='white', font=button_font, command=bookmanage_click, width=16, padx=10)
# bookManage_button.pack(side="left", padx=5)

# invenManage_button = tk.Button(button_frame, text="Inventory Management", bg='#563d2d', fg='white', font=button_font, command=Inventory_click, width=16,padx=10)
# invenManage_button.pack(side="left", padx=5)

# useracc_button = tk.Button(button_frame, text="User Account", bg='#563d2d', fg='white', font=button_font, width=10)
# useracc_button.pack(side="left",padx= 5)

# userhis_button = tk.Button(button_frame, text="User History", bg='#563d2d', fg='white',font=button_font, width=10,command=userhis_click )
# userhis_button.pack(side="left",padx= 5)

# search_button = tk.Button(button_frame, text="Search", bg='#563d2d', fg='white', font=button_font, width=10, command=search_product)
# search_button.pack(side="right", padx=12, pady=10, anchor=E)

# search_entry = tk.Entry(button_frame, font=button_font, fg='#563d2d', bg='white')
# search_entry.pack(side="right", padx=2, anchor=E)

# back_button = tk.Button(window, text="Back", bg='#563d2d', fg='white', font=button_font, command=exit_click, width=10)
# back_button.pack(side="bottom", anchor="se", padx=20, pady=10)


# # Table
# table_frame = tk.Frame(window, bg="#d3bbab")
# table_frame.pack(side="left", pady=15, padx=10, fill="both", expand=True)

# columns = ("ID", "Fullname", "Email", "Username")
# table = ttk.Treeview(table_frame, columns=columns, show="headings")
# for col in columns:
#     table.heading(col, text=col)
#     table.column(col, width=70)
# table.pack(side="left", fill="both", expand=True)

# # Scrollbar
# scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
# scrollbar.pack(side="right", fill="y")
# table.configure(yscrollcommand=scrollbar.set)

# # Populate the table with data from the database
# populate_table()

# window.mainloop()
