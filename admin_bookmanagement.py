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
window.title("Book Management")
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

def clear_entries():
    for entry in form_entries:
        entry.delete(0, 'end')

# Function to add product to the database and display in the table
def add_product():
    values = [entry.get() for entry in form_entries]
    id_value, title_value, author_value, genre_value, publisher_value, publicationdate_value, dateadded_value, bookshelf_value, quantity_value = values

    # Update the status based on the quantity
    if int(quantity_value) > 0:
        new_status = "Available"
    else:
        new_status = "Not Available"

    # Insert the new book data into the database
    cursor.execute("INSERT INTO Books (id, title, author, genre, publisher, publicationdate, dateadded, bookshelf, status, quantity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (id_value, title_value, author_value, genre_value, publisher_value, publicationdate_value, dateadded_value, bookshelf_value, new_status, quantity_value))
    connection.commit()

    # Insert the new book data into the table view
    table.insert("", "end", values=(id_value, title_value, author_value, genre_value, publisher_value, publicationdate_value, dateadded_value, bookshelf_value, quantity_value))
    clear_entries()

def edit_product():
    # Get the values from the entry fields
    id_value = form_entries[0].get()  # Assuming the ID entry is the first one in the form_entries list
    title_value = form_entries[1].get()
    author_value = form_entries[2].get()
    genre_value = form_entries[3].get()
    publisher_value = form_entries[4].get()
    publicationdate_value = form_entries[5].get()
    dateadded_value = form_entries[6].get()
    bookshelf_value = form_entries[7].get()
    quantity_value = form_entries[8].get()


    # Update the values in the table view
    selected_item = table.selection()
    if selected_item:
        current_values = table.item(selected_item, "values")
        updated_values = [
            id_value if id_value else current_values[0],
            title_value if title_value else current_values[1],
            author_value if author_value else current_values[2],
            genre_value if genre_value else current_values[3],
            publisher_value if publisher_value else current_values[4],
            publicationdate_value if publicationdate_value else current_values[5],
            dateadded_value if dateadded_value else current_values[6],
            bookshelf_value if bookshelf_value else current_values[7],
            quantity_value if quantity_value else current_values[8]
        ]
        table.item(selected_item, values=updated_values)

        # Prepare the update query
        update_query = "UPDATE Books SET "
        data = []
        if id_value:
            update_query += "id = %s, "
            data.append(id_value)
        if title_value:
            update_query += "title = %s, "
            data.append(title_value)
        if author_value:
            update_query += "author = %s, "
            data.append(author_value)
        if genre_value:
            update_query += "genre = %s, "
            data.append(genre_value)
        if publisher_value:
            update_query += "publisher = %s, "
            data.append(publisher_value)
        if publicationdate_value:
            update_query += "publicationdate = %s, "
            data.append(publicationdate_value)
        if dateadded_value:
            update_query += "dateadded = %s, "
            data.append(dateadded_value)
        if bookshelf_value:
            update_query += "bookshelf = %s, "
            data.append(bookshelf_value)
        if quantity_value:
            update_query += "quantity = %s"
            data.append(quantity_value)

        # Remove the last comma and add the WHERE clause
        update_query = update_query[:-2] + " WHERE id = %s"
        data.append(current_values[0])

        # Update the values in the database
        cursor.execute(update_query, data)
        connection.commit()
        clear_entries()
    else:
        messagebox.showinfo("Wrong","Please select a product to update")


def remv_product():
    selected_item = table.selection()
    if selected_item:
        # Delete from the database
        item_id = table.item(selected_item, "values")[0]
        cursor.execute("DELETE FROM Books WHERE id = %s", (item_id,))
        connection.commit()
        
        # Delete from the table view
        table.delete(selected_item)
    else:
        messagebox.showinfo("Wrong","Please select a product you want to delete") 

def done_product():
     # Clear the table before repopulating with all data
    for item in table.get_children():
        table.delete(item)
    # Repopulate the table with all data
    clear_entries()
    populate_table()

# Function to populate the table view with data from the database
def populate_table():
    cursor.execute("SELECT id, title, author, genre, publisher, publicationdate, dateadded, bookshelf, quantity FROM Books")
    for row in cursor.fetchall():
        table.insert("", "end", values=row)

def search_product():
    search_query = search_entry.get()
    cursor.execute("SELECT * FROM Books WHERE id = %s OR title LIKE %s", (search_query, '%' + search_query + '%'))
    # Clear the table before populating with search results
    for item in table.get_children():
        table.delete(item)
    for row in cursor.fetchall():
        table.insert("", "end", values=row)
    clear_entries()
# Button Click Functions

# def useracc_click():
#     window.destroy()
#     subprocess.run(['python', 'admin_account.py'])

def Inventory_click():
    window.destroy()
    subprocess.run(['python', 'admin_inventory.py'])

def userhis_click():
    window.destroy()
    subprocess.run(['python', 'admin_history.py'])

def exit_click():
    window.destroy()
    subprocess.run(['python', 'login.py'])

# Custom Font for Buttons
button_font = ("Lato", 14)  # Custom font for buttons
entry_font = ("Lato", 13)  # Custom font for entries

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
bookManage_button = tk.Button(button_frame, text="Book Management", bg='#563d2d', fg='white', font=button_font, width=16, padx=10)
bookManage_button.pack(side="left", padx=5)

invenManage_button = tk.Button(button_frame, text="Inventory Management", bg='#563d2d', fg='white', font=button_font, command=Inventory_click, width=16,padx=10)
invenManage_button.pack(side="left", padx=5)

# useracc_button = tk.Button(button_frame, text="User Account", bg='#563d2d', fg='white', font=button_font, command=useracc_click, width=10)
# useracc_button.pack(side="left",padx= 5)

userhis_button = tk.Button(button_frame, text="User History", bg='#563d2d', fg='white', font=button_font, width=10,command=userhis_click )
userhis_button.pack(side="left",padx= 5)

search_button = tk.Button(button_frame, text="Search", bg='#563d2d', fg='white', font=button_font, width=10, command=search_product)
search_button.pack(side="right", padx=15, pady=10, anchor=E)

search_entry = tk.Entry(button_frame, font=button_font, fg='#563d2d', bg='white')
search_entry.pack(side="right", padx=2, anchor=E)

back_button = tk.Button(window, text="Back", bg='#563d2d', fg='white', font=button_font, command=exit_click, width=10)
back_button.pack(side="bottom", anchor="se", padx=20, pady=10)

# signout_button = tk.Button(button_frame, text="Sign Out", font=button_font, command=exit_click, width=10)
# signout_button.pack(side="right", padx = 30)

# Form Fields
form_frame = tk.Frame(window, bg='#d3bbab')
form_frame.place(x=100, y=20)
form_frame.pack(side="left", padx=30)
# Add a label above the entry fields
info_label = tk.Label(form_frame, text="Information", font=("Lato", 30), bg='#d3bbab')
info_label.pack(anchor="w", pady=(0, 10))  # Add some vertical padding

form_labels = ["Book#", "Title","Author", "Genre", "Publisher", "Publication Date", "Date Added", "Self#","Quantity"]
form_entries = []

for label_text in form_labels:
    label = tk.Label(form_frame, text=label_text, font=button_font, bg='#d3bbab', padx=10)  # Increase font size for labels
    label.pack(anchor="w")
    entry = tk.Entry(form_frame, font=entry_font)  # Increase font size for entries
    entry.pack(anchor="w")
    form_entries.append(entry)

# Buttons
buttons_frame = tk.Frame(window, bg='#d3bbab')
buttons_frame.pack(side="left", padx=10)

add_button = tk.Button(buttons_frame, text="Add new", bg='#b99976', width=10, command=add_product)
add_button.pack(fill="x", padx=5, pady=10)

edit_button = tk.Button(buttons_frame, text="Edit", bg='#b99976', width=10, command=edit_product)
edit_button.pack(fill="x", padx=5, pady=10)

remv_button = tk.Button(buttons_frame, text="Remove", bg='#b99976', width=10, command=remv_product)
remv_button.pack(fill="x", padx=5, pady=10)

done_button = tk.Button(buttons_frame, text="Done", bg='#b99976', width=10, command=done_product)
done_button.pack(fill="x", padx=5, pady=10)

# Table
table_frame = tk.Frame(window, bg='#d3bbab')
table_frame.pack(side="left", padx=10, pady=30, fill="both", expand=True)

columns = ("#", "Title", "Author", "Genre", "Publisher", "Publication Date", "Date Added", "Self#","Quantity")
table = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=70)
table.pack(side="left", fill="both", expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
scrollbar.pack(side="right", fill="y")
table.configure(yscrollcommand=scrollbar.set)

# Populate the table with data from the database
populate_table()

window.mainloop()
