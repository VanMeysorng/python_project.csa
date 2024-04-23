import tkinter as tk
from tkinter import *
import mysql.connector
import os
from tkinter import messagebox
import subprocess
from PIL import ImageTk, Image
from datetime import datetime
from tkinter import ttk

# Create the main window
window = tk.Tk()
window.title("See Books")
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

cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS UserHistory (id INT AUTO_INCREMENT PRIMARY KEY,userID VARCHAR(100), book_id VARCHAR(100), book_title VARCHAR(255), book_author VARCHAR(255), book_genre VARCHAR(255), transaction_date VARCHAR(100), transaction_type VARCHAR(255))")

# Custom Font for Buttons
button_font = ("Lato", 15)  
entry_font = ("Lato", 12)  

# Retrieving the user_id from the file
with open('userId.txt', 'r') as file:
    userID = int(file.read())
   
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
            update_logged_in_status(cursor, userID, 0)  
            conn.commit()
            userID = None  

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {str(err)}")
    window.destroy()  # Close the application

def search_book():
    search_query = search_entry.get()
    if not search_query:  
        for item in table.get_children():
            table.delete(item)
        populate_table()  # Repopulate the table with all data
    else:
        # Search by id or title
        cursor.execute("SELECT id, title, author, genre, publisher, publicationdate, status FROM Books WHERE id = %s OR title LIKE %s", (search_query, '%' + search_query + '%'))
        for item in table.get_children():
            table.delete(item)
        for row in cursor.fetchall():
            table.insert("", "end", values=row)

def show_receipt(values, transaction_type, userID):
    receipt_window = tk.Toplevel(window)
    receipt_window.title("Receipt")
    receipt_window.geometry('350x250')
    receipt_window.resizable(False, False)
    receipt_window.configure(bg="#d3bbab")

    # Retrieve the username from the user_account table based on the user_id
    cursor.execute("SELECT username FROM user_account WHERE id = %s", (userID,))
    result = cursor.fetchone()
    if result:
        username = result[0]
    else:
        username = "Unknown"  

    # Create and pack labels to display the receipt information
    receipt_label = tk.Label(receipt_window, text="Your Book is Here:", font=("Lato", 15), bg='#d3bbab', fg='#563d2d')
    receipt_label.pack()

    user_label = tk.Label(receipt_window, text="User: " + username, font=("Lato", '12'), bg='#d3bbab')
    user_label.pack()

    for i in range(len(form_labels)):
        entry_label = tk.Label(receipt_window, text=form_labels[i] + ": " + values[i], font=("Lato", 12), bg='#d3bbab')
        entry_label.pack()

    transaction_date_label = tk.Label(receipt_window, text="Transaction Date: " + date, font=("Lato", 12), bg="#d3bbab")
    transaction_date_label.pack()

    transaction_type_label = tk.Label(receipt_window, text="Transaction Type: " + transaction_type, font=("Lato", 12), bg='#d3bbab')
    transaction_type_label.pack()

    close_button = tk.Button(receipt_window, text="Close", command=receipt_window.destroy, bg='#563d2d', fg='white')
    close_button.pack()

def add_book():
    values = [entry.get() for entry in form_entries]
    transaction_type = transaction_type_combobox.get()  
    book_id = values[0]  

    # Check if the user entries match the id, title, and author from the books table
    cursor.execute("SELECT id, title, author, quantity, status FROM Books WHERE id = %s", (book_id,))
    book_data = cursor.fetchone()

    if book_data:
        current_quantity = int(book_data[3])  

        if transaction_type == "Return":
            new_quantity = str(current_quantity + 1) 
            cursor.execute("UPDATE Books SET quantity = %s WHERE id = %s", (new_quantity, book_id))
            connection.commit()

            # Update the status based on the quantity
            if int(new_quantity) > 0:
                new_status = "Available"
            else:
                new_status = "Unavailable"
            cursor.execute("UPDATE Books SET status = %s WHERE id = %s", (new_status, book_id))
            connection.commit()

            user_history_values = [userID, book_id, values[1], values[2], values[3], date, transaction_type]  
            cursor.execute("INSERT INTO userhistory (userID, bookID, book_title, book_author, book_genre, transaction_date, transaction_type) VALUES (%s, %s, %s, %s, %s, %s, %s)", user_history_values)
            connection.commit()
            clear_entries()
            show_receipt(values, transaction_type, userID)
            update_table_row(book_id, new_status) 
        elif transaction_type == "Issue":
            if current_quantity > 0:  
                new_quantity = str(current_quantity - 1) 
                cursor.execute("UPDATE Books SET quantity = %s WHERE id = %s", (new_quantity, book_id))
                connection.commit()

                if int(new_quantity) > 0:
                    new_status = "Available"
                else:
                    new_status = "Unavailable"
                cursor.execute("UPDATE Books SET status = %s WHERE id = %s", (new_status, book_id))
                connection.commit()

                user_history_values = [userID, book_id, values[1], values[2], values[3], date, transaction_type]  
                cursor.execute("INSERT INTO userhistory (userID, bookID, book_title, book_author, book_genre, transaction_date, transaction_type) VALUES (%s, %s, %s, %s, %s, %s, %s)", user_history_values)
                connection.commit()
                clear_entries()

                show_receipt(values, transaction_type, userID)
                update_table_row(book_id, new_status)  
            else:
                messagebox.showerror("Error", "No available copies to issue")
    else:
        messagebox.showerror("Error", "No matching book found in the database.")

def update_table_row(book_id, new_status):
    for item in table.get_children():
        if table.item(item, "values")[0] == book_id:
            row_values = table.item(item, "values")
            updated_values = (
                row_values[0],
                row_values[1],
                row_values[2],
                row_values[3],
                row_values[4],
                row_values[5],
                new_status,
            )
            table.item(item, values=updated_values)
            break

def update_logged_in_status(cursor, userID, status):
    update_sql = "UPDATE user_account SET logged_in = %s WHERE id = %s"
    cursor.execute(update_sql, (status, userID))
    
def get_logged_in_userID():
    cursor.execute("SELECT id FROM user_account WHERE logged_in = 1")
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return ""
    
def clear_entries():
    for entry in form_entries:
        entry.delete(0, 'end')

def show_book():
    for item in table.get_children():
        table.delete(item)
    clear_entries()
    update_table_row()

def populate_table():
    cursor.execute("SELECT id, title, author, genre, publisher, publicationdate, status FROM Books")    
    for row in cursor.fetchall():
        table.insert("", "end", values=row)

def acc_click():
    window.destroy()
    subprocess.run(['python', 'user_acc.py'])

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
seebook_button = tk.Button(button_frame, text="See Books", bg='#563d2d', fg='white', font=button_font, width=16, padx=10)
seebook_button.pack(side="left", padx=10)

acc_button = tk.Button(button_frame, text="My Account", bg='#563d2d', fg='white', command=acc_click, font=button_font,  width=16, padx=10)
acc_button.pack(side="left", padx=10)

search_button = tk.Button(button_frame, text="Search", bg='#563d2d', fg='white', font=button_font, width=10, command=search_book)
search_button.pack(side="right", padx=10, pady=10)

search_entry = tk.Entry(button_frame, font=button_font, fg='#563d2d', bg='white',)
search_entry.pack(side="right", padx=25)

back_button = tk.Button(window, text="Back", font=button_font, width=10, command=exit_click, bg='#563d2d', fg='white',)
back_button.pack(side="bottom", anchor="se", padx=20, pady=10)

# Table
table_frame = tk.Frame(window, bg="#d3bbab")
table_frame.pack(side="left", pady=18,padx=20, fill="both", expand=True, anchor="nw")

columns = ("#Book", "Title", "Author", "Genre", "Publisher", "Publication Date", "Status")
table = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=70)
table.pack(side="left", fill="both", expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
scrollbar.pack(side="right", fill="y")
table.configure(yscrollcommand=scrollbar.set)

# Form Fields
form_frame = tk.Frame(window, bg="#d3bbab")
form_frame.place(x=100, y=20)
form_frame.pack(side="left", padx=0)
# Add a label above the entry fields
info_label = tk.Label(form_frame, text="Your Book", font=("Lato", 30), bg="#d3bbab")
info_label.pack(anchor="w", pady=(10, 20)) 

form_labels = [ "Book#","Title","Author", "Genre"]
form_entries = []

for label_text in form_labels:
    label = tk.Label(form_frame, text=label_text, font=button_font, bg="#d3bbab")  
    label.pack(anchor="w")
    entry = tk.Entry(form_frame, font=entry_font) 
    entry.pack(anchor="w")
    form_entries.append(entry)
date_pr = StringVar()
date_pr.set(datetime.now())
date = date_pr.get()

transaction_date_label = tk.Label(form_frame, text="Transaction Date", font=("Lato", 15), bg="#d3bbab").pack(anchor="w")
transaction_date_entry = Entry(form_frame, textvariable = date_pr, font= ("Arial", 15), width=23)
transaction_date_entry.pack(anchor="w", pady=(0, 10))

transaction_type_label = tk.Label(form_frame, text="Transaction Type", font=("Lato", 15), bg="#d3bbab")
transaction_type_label.pack(anchor="w")

transaction_type_combobox = ttk.Combobox(form_frame, values=["Issue","Return"], font=("Lato", 15))
transaction_type_combobox.pack(anchor="w", pady=(0, 10))  

# Buttons
buttons_frame = tk.Frame(window, bg="#d3bbab")
buttons_frame.pack(side="left", padx=20)

add_button = tk.Button(buttons_frame, text="Done", width=10,command=add_book, font=("Lato", 10), fg='black', bg="#b99976")
add_button.pack(fill="x", padx=5, pady=10)

# Populate the table with data from the database
populate_table()
window.protocol("WM_DELETE_WINDOW", sign_out) 

window.mainloop()