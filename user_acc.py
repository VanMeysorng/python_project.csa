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

# Custom Font for Buttons
button_font = ("Lato", 15)  # Custom font for buttons
entry_font = ("Lato", 12)  # Custom font for entries

# Retrieving the user_id from the file
with open('userID.txt', 'r') as file:
    userID = int(file.read())

def search_product():
    search_query = search_entry.get()
    if not search_query:  # If the search query is empty, repopulate the table with all records
        for item in table.get_children():
            table.delete(item)
        populate_user_history_table(userID)
    else:
        cursor.execute("SELECT book_id, book_title, book_author, book_genre, transaction_date, transaction_type FROM userhistory WHERE book_id = %s OR book_title LIKE %s", (search_query, '%' + search_query + '%'))
        for item in table.get_children():
            table.delete(item)
        for row in cursor.fetchall():
            table.insert("", "end", values=row)



def populate_user_history_table(userID):
    try:
        cursor.execute("SELECT book_id, book_title, book_author, book_genre, transaction_date, transaction_type FROM userhistory WHERE userID = %s", (userID,))
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

# def update_username_label():
#     # Retrieve the username of the logged-in user
#     username = get_logged_in_username()
#     # Update the username label with the retrieved username
#     username_label.config(text="Hi, " + username + "!")
#     # Schedule the function to run again after a delay (e.g., 1 second)
#     username_label.after(1000, update_username_label)

def seeacc_btn():
    window.destroy()
    subprocess.run(['python', 'user_book.py'])
# Retrieving the user_id from the file

def sign_out():
    # Retrieving the user_id from the file
    with open('userID.txt', 'r') as file:
        userID = int(file.read())

    if userID:
        try:
            conn = mysql.connector.connect(
                user="root",
                password="ms123456",
                host="localhost",
                database="Library"
            )

            cursor = conn.cursor()
            update_logged_in_status(cursor, userID, 0)  # Set logged_in status to 0 for the logged-out user
            conn.commit()
            userID = None  # Reset the user ID

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {str(err)}")
    window.destroy()  # Close the application


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
        update_logged_in_status(cursor, userID, 0)  # Set logged_in status to 0 for the logged-out user
        conn.commit()
        window.destroy()  # Close the application
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


# Buttons for Products, Customers, Manage, Exit
seebook_button = tk.Button(button_frame, text="See Books", bg='#563d2d', fg='white', font=button_font, width=16, padx=10, command=seeacc_btn)
seebook_button.pack(side="left", padx=10)

acc_button = tk.Button(button_frame, text="My Account", bg='#563d2d', fg='white', font=button_font,  width=16, padx=10)
acc_button.pack(side="left", padx=10)

search_button = tk.Button(button_frame, text="Search", bg='#563d2d', fg='white', font=button_font, width=10, command=search_product)
search_button.pack(side="right", padx=10, pady=10)

search_entry = tk.Entry(button_frame, font=button_font, fg='#563d2d', bg='white',)
search_entry.pack(side="right", padx=25)

back_button = tk.Button(window, text="Back", font=button_font, width=10, command=exit_click, bg='#563d2d', fg='white',)
back_button.pack(side="bottom", anchor="se", padx=20, pady=15)

# Username Label
username = get_logged_in_username()
username_label = tk.Label(window, text="Hi, " + username + "!", bg="#d3bbab", font=("Lato", 35))
username_label.pack(side="left", pady=0, anchor="w", padx=8)


# # Call the function to update the username label
# update_username_label()

# Icon image
icon_image = Image.open("icon.png")
icon_image = icon_image.resize((150, 150))
icon_image = ImageTk.PhotoImage(icon_image)
icon_label = tk.Label(image=icon_image, bg="#d3bbab")
icon_label.pack(side="left", pady=0, anchor="w", padx=0)

# Table
table_frame = tk.Frame(window,bg="#d3bbab")
table_frame.pack(side="left", padx=15, fill="both", expand=True,)

columns = ("#", "Title", "Author", "Genre", "Transition Date", "Transition Type")
table = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=70)
table.pack(side="left", fill="both", expand=True,pady=25)

# Scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
scrollbar.pack(side="right", fill="y", pady=25)
table.configure(yscrollcommand=scrollbar.set)

# Populate the table with data from the database
populate_user_history_table(userID)
window.protocol("WM_DELETE_WINDOW", sign_out)  # Bind exit_click to window close

window.mainloop()