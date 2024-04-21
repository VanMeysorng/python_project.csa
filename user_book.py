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
window.title("See Books")
window.geometry('1200x680+300+200')
window.resizable(False, False)
window.configure(bg="#d3bbab")

# Establish Connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Chetra1234",  # Change it to your password
    database="Library"
)
# Create a cursor
cursor = connection.cursor()
# Create UserHistory table
cursor.execute("CREATE TABLE IF NOT EXISTS UserHistory (id INT AUTO_INCREMENT PRIMARY KEY,user_id VARCHAR(100), book_id VARCHAR(100), book_title VARCHAR(255), book_author VARCHAR(255), book_genre VARCHAR(255), transaction_date VARCHAR(100), transaction_type VARCHAR(255))")

# Custom Font for Buttons
button_font = ("Lato", 15)  # Custom font for buttons
entry_font = ("Lato", 12)  # Custom font for entries

# Retrieving the user_id from the file
with open('user_id.txt', 'r') as file:
    user_id = int(file.read())
   
def sign_out():
    # Retrieving the user_id from the file
    with open('user_id.txt', 'r') as file:
        user_id = int(file.read())

    if user_id:
        try:
            conn = mysql.connector.connect(
                user="root",
                password="Chetra1234",
                host="localhost",
                database="Library"
            )

            cursor = conn.cursor()
            update_logged_in_status(cursor, user_id, 0)  # Set logged_in status to 0 for the logged-out user
            conn.commit()
            user_id = None  # Reset the user ID

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {str(err)}")
    window.destroy()  # Close the application

def search_product():
    search_query = search_entry.get()
    if not search_query:  # If the search query is empty, repopulate the table with all records
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

def show_receipt(values, transaction_type, user_id):
    receipt_window = tk.Toplevel(window)
    receipt_window.title("Receipt")
    receipt_window.geometry('300x300')
    receipt_window.resizable(False, False)
    receipt_window.configure(bg="#d3bbab")

    # Retrieve the username from the user_account table based on the user_id
    cursor.execute("SELECT username FROM user_account WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    if result:
        username = result[0]
    else:
        username = "Unknown"  # Default username if not found

    # Create and pack labels to display the receipt information
    receipt_label = tk.Label(receipt_window, text="Your Book Here:", font=("Lato", 15), bg='#d3bbab', fg='#563d2d')
    receipt_label.pack()

    user_label = tk.Label(receipt_window, text="User: " + username, font=("Lato", '12'), bg='#d3bbab')
    user_label.pack()

    for i in range(len(form_labels)):
        entry_label = tk.Label(receipt_window, text=form_labels[i] + ": " + values[i], font=("Lato", 12))
        entry_label.pack()

    transaction_type_label = tk.Label(receipt_window, text="Transaction Type: " + transaction_type, font=("Lato", 12), bg='#d3bbab')
    transaction_type_label.pack()

    close_button = tk.Button(receipt_window, text="Close", command=receipt_window.destroy, bg='#563d2d', fg='white')
    close_button.pack()

def add_product():
    values = [entry.get() for entry in form_entries]
    transaction_type = transaction_type_combobox.get()  # Get the selected value from the combobox
    book_id = values[0]  # Assuming the first entry field is for book ID

    # Check if the user entries match the id, title, and author from the books table
    cursor.execute("SELECT id, title, author, quantity, status FROM Books WHERE id = %s", (book_id,))
    book_data = cursor.fetchone()

    if book_data:
        current_quantity = int(book_data[3])  # Convert the quantity from string to integer

        if transaction_type == "Return":
            # Increase the quantity by one
            new_quantity = str(current_quantity + 1)  # Convert back to string for database update
            # Update the quantity in the Books table
            cursor.execute("UPDATE Books SET quantity = %s WHERE id = %s", (new_quantity, book_id))
            connection.commit()

            # Update the status based on the quantity
            if int(new_quantity) > 0:
                new_status = "Available"
            else:
                new_status = "Unavailable"
            cursor.execute("UPDATE Books SET status = %s WHERE id = %s", (new_status, book_id))
            connection.commit()

            # Store the user-specific data in the UserHistory table
            user_history_values = [user_id, book_id, values[1], values[2], values[3], values[4], transaction_type]  # Extract the necessary values from 'values' list
            cursor.execute("INSERT INTO UserHistory (user_id, book_id, book_title, book_author, book_genre, transaction_date, transaction_type) VALUES (%s, %s, %s, %s, %s, %s, %s)", user_history_values)
            connection.commit()
            clear_entries()
            # After updating the database and clearing the entries, show the receipt
            show_receipt(values, transaction_type, user_id)
            update_table_row(book_id, new_status)  # Update the specific row in the table view with the new status
        elif transaction_type == "Issue":
            if current_quantity > 0:  # Check if there are available copies to issue
                # Decrease the quantity by one
                new_quantity = str(current_quantity - 1)  # Convert back to string for database update
                # Update the quantity in the Books table
                cursor.execute("UPDATE Books SET quantity = %s WHERE id = %s", (new_quantity, book_id))
                connection.commit()

                # Update the status based on the quantity
                if int(new_quantity) > 0:
                    new_status = "Available"
                else:
                    new_status = "Unavailable"
                cursor.execute("UPDATE Books SET status = %s WHERE id = %s", (new_status, book_id))
                connection.commit()

                # Store the user-specific data in the UserHistory table
                user_history_values = [user_id, book_id, values[1], values[2], values[3], values[4], transaction_type]  # Extract the necessary values from 'values' list
                cursor.execute("INSERT INTO UserHistory (user_id, book_id, book_title, book_author, book_genre, transaction_date, transaction_type) VALUES (%s, %s, %s, %s, %s, %s, %s)", user_history_values)
                connection.commit()
                clear_entries()
                # After updating the database and clearing the entries, show the receipt
                show_receipt(values, transaction_type, user_id)
                update_table_row(book_id, new_status)  # Update the specific row in the table view with the new status
            else:
                messagebox.showerror("Error", "No available copies to issue")
    else:
        messagebox.showerror("Error", "No matching book found in the database.")

def update_table_row(book_id, new_status):
    # Find the item in the table view with the corresponding book_id
    for item in table.get_children():
        if table.item(item, "values")[0] == book_id:
            # Update the status for the specific row while keeping other values unchanged
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

def update_logged_in_status(cursor, user_id, status):
    update_sql = "UPDATE user_account SET logged_in = %s WHERE id = %s"
    cursor.execute(update_sql, (status, user_id))
    
def get_logged_in_user_id():
    # Retrieve the username from the user_account table based on the logged-in user
    cursor.execute("SELECT id FROM user_account WHERE logged_in = 1")
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return ""
    
def clear_entries():
    for entry in form_entries:
        entry.delete(0, 'end')

def show_product():
     # Clear the table before repopulating with all data
    for item in table.get_children():
        table.delete(item)
    # Repopulate the table with all data
    clear_entries()
    update_table_row()
# Function to populate the table view with data from the database
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
            password="Chetra1234",
            host="localhost",
            database="Library"
        )

        cursor = conn.cursor()
        update_logged_in_status(cursor, user_id, 0)  # Set logged_in status to 0 for the logged-out user
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
seebook_button = tk.Button(button_frame, text="See Books", bg='#563d2d', fg='white', font=button_font, width=16, padx=10)
seebook_button.pack(side="left", padx=10)

acc_button = tk.Button(button_frame, text="My Account", bg='#563d2d', fg='white', command=acc_click, font=button_font,  width=16, padx=10)
acc_button.pack(side="left", padx=10)

search_button = tk.Button(button_frame, text="Search", bg='#563d2d', fg='white', font=button_font, width=10, command=search_product)
search_button.pack(side="right", padx=10, pady=10)

search_entry = tk.Entry(button_frame, font=button_font, fg='#563d2d', bg='white',)
search_entry.pack(side="right", padx=25)

back_button = tk.Button(window, text="Back", font=button_font, width=10, command=exit_click, bg='#563d2d', fg='white',)
back_button.pack(side="bottom", anchor="se", padx=20, pady=10)
# signout_button = tk.Button(button_frame, text="Sign Out", font=button_font, command=exit_click, width=10)
# signout_button.pack(side="right", padx = 30)

# Table
table_frame = tk.Frame(window, bg="#d3bbab")
# Modify the table_frame widget's pack method parameters
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
info_label.pack(anchor="w", pady=(10, 20))  # Add some vertical padding

form_labels = [ "Book#","Title","Author", "Genre", "Transaction Date"]
form_entries = []

for label_text in form_labels:
    label = tk.Label(form_frame, text=label_text, font=button_font, bg="#d3bbab")  # Increase font size for labels
    label.pack(anchor="w")
    entry = tk.Entry(form_frame, font=entry_font)  # Increase font size for entries
    entry.pack(anchor="w")
    form_entries.append(entry)

transaction_type_label = tk.Label(form_frame, text="Transaction Type:", font=("Lato", 15), bg="#d3bbab")
transaction_type_label.pack(anchor="w")

transaction_type_combobox = ttk.Combobox(form_frame, values=["Issue","Return"], font=("Lato", 15))
transaction_type_combobox.pack(anchor="w", pady=(0, 10))  # Add some vertical padding

# Buttons
buttons_frame = tk.Frame(window, bg="#d3bbab")
buttons_frame.pack(side="left", padx=20)

add_button = tk.Button(buttons_frame, text="Add New", width=10,command=add_product, font=("Lato", 10), fg='black', bg="#b99976")
add_button.pack(fill="x", padx=5, pady=10)

# Populate the table with data from the database
populate_table()
window.protocol("WM_DELETE_WINDOW", sign_out)  # Bind exit_click to window close

window.mainloop()