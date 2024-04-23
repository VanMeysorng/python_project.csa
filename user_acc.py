import tkinter as tk
from tkinter import *
import mysql.connector
import os
from tkinter import messagebox
import subprocess
from PIL import ImageTk, Image


from tkinter import ttk

# Create the main window
window = tk.Tk()
window.title("My Account")
window.geometry('1200x680+300+200')
window.resizable(False, False)
window.configure(bg="#d3bbab")

# Establish Connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ms123456",  # Change it to your password
    database="Library"
)

# Create a cursor
cursor = connection.cursor()

# Custom Font for Buttons and Entries
button_font = ("Lato", 15)  
entry_font = ("Lato", 12)  

# Retrieving the user_id from the file
with open('userID.txt', 'r') as file:
    userID = int(file.read())

def search_book():
    search_query = search_entry.get()
    if not search_query:  
        for item in table.get_children():
            table.delete(item)
        populate_user_history_table(userID)
    else:
        cursor.execute("SELECT userID, bookID, book_title, book_author, book_genre, transaction_date, transaction_type FROM userhistory WHERE (userID = %s) AND (bookID = %s OR book_title LIKE %s)",
                       (userID, search_query, '%' + search_query + '%'))
        for item in table.get_children():
            table.delete(item)
        for row in cursor.fetchall():
            table.insert("", "end", values=row)


def populate_user_history_table(userID):
    try:
        cursor.execute("SELECT userID, bookID, book_title, book_author, book_genre, transaction_date, transaction_type FROM userhistory WHERE userID = %s", (userID,))
        results = cursor.fetchall()

        for row in results:
            table.insert("", "end", values=row)

    except mysql.connector.Error as err:
        print(f"An error occurred: {str(err)}")

# Function to retrieve the username of the logged-in user
def get_logged_in_username():
    cursor.execute("SELECT username FROM user_account WHERE id = %s", (userID,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return ""

def seeacc_btn():
    window.destroy()
    subprocess.run(['python', 'user_book.py'])
 


def update_logged_in_status(cursor, userID, status):
    update_sql = "UPDATE user_account SET logged_in = %s WHERE id = %s"
    cursor.execute(update_sql, (status, userID))


def exit_click():
    try:
        conn = mysql.connector.connect(
            user="root",
            password="ms123456",
            host="localhost",
            database="Library"
        )

        cursor = conn.cursor()
        update_logged_in_status(cursor, userID, 0)  
        conn.commit()
        window.destroy() 
        subprocess.run(['python', 'login.py'])


    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"An error occurred: {str(err)}")

# Frame for Buttons
button_frame = tk.Frame(window, bg="#3d291f")
button_frame.pack(side="top", fill="x", padx=0, pady=0)

# Logo
logo_image = Image.open("bookstack_logo.png")
logo_image = logo_image.resize((50, 60))
logo_image = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(button_frame, image=logo_image, highlightthickness=0, bd=0, bg="#3d291f", compound=tk.LEFT)
logo_label.pack(side="left", padx=0, pady=0, anchor="nw")

# Buttons 
seebook_button = tk.Button(button_frame, text="See Books", bg='#563d2d', fg='white', font=button_font, width=16, padx=10, command=seeacc_btn)
seebook_button.pack(side="left", padx=10)

acc_button = tk.Button(button_frame, text="My Account", bg='#563d2d', fg='white', font=button_font,  width=16, padx=10)
acc_button.pack(side="left", padx=10)

search_button = tk.Button(button_frame, text="Search", bg='#563d2d', fg='white', font=button_font, width=10, command=search_book)
search_button.pack(side="right", padx=10, pady=10)

search_entry = tk.Entry(button_frame, font=button_font, fg='#563d2d', bg='white',)
search_entry.pack(side="right", padx=25)

back_button = tk.Button(window, text="Back", font=button_font, width=10, command=exit_click, bg='#563d2d', fg='white',)
back_button.pack(side="bottom", anchor="se", padx=20, pady=15)

# Frame to contain username label and icon label
user_frame = tk.Frame(window, bg="#d3bbab")
user_frame.pack(side="left", padx=10)

# Icon image
icon_image = Image.open("icon.png")
icon_image = icon_image.resize((150, 150))
icon_image = ImageTk.PhotoImage(icon_image)
icon_label = tk.Label(user_frame, image=icon_image, bg="#d3bbab")
icon_label.pack(side="top", pady=0, anchor="nw", padx=30)

# Username Label
username = get_logged_in_username()
username_label = tk.Label(user_frame, text="Hi, " + username + "!", bg="#d3bbab", font=("Lato", 35))
username_label.pack(side="left", pady=0, anchor="nw", padx=15)

# Table
table_frame = tk.Frame(window,bg="#d3bbab")
table_frame.pack(side="left", padx=15, fill="both", expand=True,)

columns = ("#User", "#Book", "Title", "Author", "Genre", "Transition Date", "Transition Type")
table = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=70)
table.pack(side="left", fill="both", expand=True,pady=25)

# Scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
scrollbar.pack(side="right", fill="y", pady=25)
table.configure(yscrollcommand=scrollbar.set)

populate_user_history_table(userID)

window.mainloop()