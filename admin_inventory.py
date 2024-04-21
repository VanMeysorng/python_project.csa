import tkinter as tk
from tkinter import *
from tkinter import ttk
import mysql.connector
import os
from PIL import ImageTk, Image
import subprocess
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create the main window
window = tk.Tk()
window.title("User History")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 1500
window_height = 850
window_pos_x = int((screen_width - window_width) / 2)
window_pos_y = int((screen_height - window_height) / 2)
window.geometry(f'{window_width}x{window_height}+{window_pos_x}+{window_pos_y}')
window.configure(bg="#d3bbab")
window.resizable(False, False)

# Establish Connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ms123456",  # Change it to your password
    database="Library"
)

# Create a cursor
cursor = connection.cursor()

# Function to populate the table view with data from the database
def populate_table():
    cursor.execute("SELECT user_account.id, user_account.full_name, user_account.email, user_account.username, UserHistory.transaction_date, UserHistory.transaction_type FROM user_account LEFT JOIN UserHistory ON user_account.id = UserHistory.user_id")
    for row in cursor.fetchall():
        table.insert("", "end", values=row)

def search_product():
    search_query = search_entry.get()
    # Clear the table before populating with search results
    for item in table.get_children():
        table.delete(item)
    # Execute the SQL query with the search condition
    cursor.execute("SELECT user_account.id, user_account.full_name, user_account.email, user_account.username, UserHistory.transaction_date, UserHistory.transaction_type FROM user_account LEFT JOIN UserHistory ON user_account.id = UserHistory.user_id WHERE user_account.full_name LIKE %s", (f'%{search_query}%',))
    # Populate the table with the search results
    for row in cursor.fetchall():
        table.insert("", "end", values=row)


# Button Click Functions
def bookmanage_click():
    window.destroy()
    subprocess.run(['python', 'admin_bookmanagement.py'])

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
button_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

# Logo
logo_image = Image.open("bookstack_logo.png")
logo_image = logo_image.resize((60, 70))
logo_image = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(button_frame, image=logo_image, highlightthickness=0, bd=0, bg="#3d291f", compound=tk.LEFT)
logo_label.pack(side="left", padx=0, pady=0, anchor="nw")

# Buttons for Products, Customers, Manage, Exit
bookManage_button = tk.Button(button_frame, text="Book Management", bg='#563d2d', fg='white', font=button_font, command=bookmanage_click, width=16, padx=10)
bookManage_button.pack(side="left", padx=5)

invenManage_button = tk.Button(button_frame, text="Inventory Management", bg='#563d2d', fg='white', font=button_font, width=16,padx=10)
invenManage_button.pack(side="left", padx=5)

userhis_button = tk.Button(button_frame, text="User History", bg='#563d2d', fg='white', font=button_font, command=userhis_click, width=10)
userhis_button.pack(side="left", padx=5)

search_button = tk.Button(button_frame, text="Search", bg='#563d2d', fg='white', font=button_font, width=10, command=search_product)
search_button.pack(side="right", padx=12, pady=10, anchor=E)

search_entry = tk.Entry(button_frame, font=button_font, fg='#563d2d', bg='white')
search_entry.pack(side="right", padx=2, anchor=E)

back_button = tk.Button(window, text="Back", bg='#563d2d', fg='white', font=button_font, command=exit_click, width=10)
back_button.grid(row=2, column=1, sticky="se", padx=20, pady=10)

# Table Frame
table_frame = tk.Frame(window, bg="#d3bbab")
table_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

columns = ("#", "Title", "Author", "Genre", "Quantity", "Status")
table = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=70)
table.pack(side="left", fill="both", expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
scrollbar.pack(side="right", fill="y")
table.configure(yscrollcommand=scrollbar.set)

# Labels Frame
labels_frame = tk.Frame(window, bg="white")
labels_frame.grid(row=1, column=0, sticky="nw", padx=20, pady=20)

# Create the labels for total books and total users inside the frame
total_font = ("Lato", 35)

total_users_label = tk.Label(labels_frame, text="Total Users: ", font=total_font, bg="white", fg='#3d291f')
total_users_label.pack(side="top", anchor='w', padx=10, pady=10)

total_books_label = tk.Label(labels_frame, text="Total Books: ", font=total_font, bg="white", fg='#3d291f')
total_books_label.pack(side="top", anchor='w', padx=10, pady=10)

# Function to update the total books and total users labels
def update_totals():
    # Retrieve the sum of quantities from the Books table
    cursor.execute("SELECT SUM(quantity) FROM Books")
    total_books = cursor.fetchone()[0]
    if total_books:
        total_books = int(total_books)
    else:
        total_books = 0

    # Retrieve the total number of user accounts from the user_account table
    cursor.execute("SELECT COUNT(*) FROM user_account")
    total_users = cursor.fetchone()[0]

    # Update the labels with the retrieved values
    total_books_label.config(text="Total Books: " + str(total_books))
    total_users_label.config(text="Total Users: " + str(total_users))
# Call the update_totals function initially to display the initial values
update_totals()

# Function to generate and display the bar chart
def generate_bar_chart():
    # Fetch data from the UserHistory table
    cursor.execute("SELECT transaction_type, COUNT(*) FROM UserHistory GROUP BY transaction_type")
    results = cursor.fetchall()

    # Separate the data into two lists: transaction types and counts
    transaction_types = [result[0] for result in results]
    counts = [result[1] for result in results]

    # Create the bar chart with specified figure size
    fig, ax = plt.subplots(figsize=(6, 5))  # Adjust the figure size as per your preference
    ax.bar(transaction_types, counts)
    ax.set_xlabel('Transaction Type')
    ax.set_ylabel('Count')
    ax.set_title('Transaction Types: Issued vs. Returned')

    # Set the y-axis range from 0 to the maximum count + 1
    ax.set_ylim(0, max(counts) + 1)

    # Create a FigureCanvasTkAgg instance and embed the chart in the window
    chart_canvas = FigureCanvasTkAgg(fig, master=window)
    chart_canvas.draw()
    # Adjust the position and padding as per your requirement
    chart_canvas.get_tk_widget().grid(row=1, column=0, sticky="sw", padx=20, pady=13)

# Call the function to generate and display the bar chart
generate_bar_chart()

# Populate the table with data from the database
populate_table()

# Configure row and column weights for resizing
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(1, weight=1)

window.mainloop()
