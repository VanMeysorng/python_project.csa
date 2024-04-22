# import tkinter as tk
# from tkinter import *
# import mysql.connector
# import os
# from tkinter import messagebox
# import subprocess
# from PIL import ImageTk, Image
# import matplotlib.pyplot as plt
# from tkinter import ttk
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# # Create the main window
# window = tk.Tk()
# window.title("Inventory Management")
# window.geometry('1200x1000+300+200')
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
# # Create UserHistory table
# cursor.execute("CREATE TABLE IF NOT EXISTS UserHistory (id INT AUTO_INCREMENT PRIMARY KEY,user_id VARCHAR(100), book_id VARCHAR(100), book_title VARCHAR(255), book_author VARCHAR(255), book_genre VARCHAR(255), transaction_date VARCHAR(100), transaction_type VARCHAR(255))")

# # Retrieving the user_id from the file
# with open('user_id.txt', 'r') as file:
#     user_id = int(file.read())
   
# def sign_out():
#     # Retrieving the user_id from the file
#     with open('user_id.txt', 'r') as file:
#         user_id = int(file.read())

#     if user_id:
#         try:
#             conn = mysql.connector.connect(
#                 user="root",
#                 password="Chetra1234",
#                 host="localhost",
#                 database="Library"
#             )

#             cursor = conn.cursor()
#             update_logged_in_status(cursor, user_id, 0)  # Set logged_in status to 0 for the logged-out user
#             conn.commit()
#             user_id = None  # Reset the user ID

#         except mysql.connector.Error as err:
#             messagebox.showerror("Error", f"An error occurred: {str(err)}")
#     window.destroy()  # Close the application


# def update_logged_in_status(cursor, user_id, status):
#     update_sql = "UPDATE user_account SET logged_in = %s WHERE id = %s"
#     cursor.execute(update_sql, (status, user_id))
    
# def get_logged_in_user_id():
#     # Retrieve the username from the user_account table based on the logged-in user
#     cursor.execute("SELECT id FROM user_account WHERE logged_in = 1")
#     result = cursor.fetchone()
#     if result:
#         return result[0]
#     else:
#         return ""
    
# # def clear_entries():
# #     for entry in form_entries:
# #         entry.delete(0, 'end')

# # def show_product():
# #      # Clear the table before repopulating with all data
# #     for item in table.get_children():
# #         table.delete(item)
# #     # Repopulate the table with all data
# #     clear_entries()
# #     populate_table()

# # Function to populate the table view with data from the database
# def populate_table():
#     cursor.execute("SELECT id, title, author, genre, quantity, status FROM Books")
#     for item in table.get_children():
#         table.delete(item)
#     for row in cursor.fetchall():
#         table.insert("", "end", values=row)

# def search_product():
#     search_query = search_entry.get()
#     if search_query:  # If the search query is not empty
#         cursor.execute("SELECT id, title, author, genre, quantity, status FROM Books WHERE id = %s", (search_query,))
#     else:  # If the search query is empty, retrieve all data
#         cursor.execute("SELECT id, title, author, genre, quantity, status FROM Books")

#     # Clear the table before populating with search results
#     for item in table.get_children():
#         table.delete(item)
#     for row in cursor.fetchall():
#         table.insert("", "end", values=row)


# def bookmanage_click():
#     window.destroy()
#     subprocess.run(['python', 'admin_bookmanagement.py'])

# # def useracc_click():
# #     window.destroy()
# #     subprocess.run(['python', 'admin_account.py'])

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

# invenManage_button = tk.Button(button_frame, text="Inventory Management", bg='#563d2d', fg='white', font=button_font, width=16,padx=10)
# invenManage_button.pack(side="left", padx=5)

# # useracc_button = tk.Button(button_frame, text="User Account", bg='#563d2d', fg='white', font=button_font, width=10,command=useracc_click)
# # useracc_button.pack(side="left",padx= 5)

# userhis_button = tk.Button(button_frame, text="User History", bg='#563d2d', fg='white', font=button_font, width=10,command=userhis_click )
# userhis_button.pack(side="left",padx= 5)

# search_button = tk.Button(button_frame, text="Search", bg='#563d2d', fg='white', font=button_font, width=10, command=search_product)
# search_button.pack(side="right", padx=12, pady=10, anchor=E)

# search_entry = tk.Entry(button_frame, font=button_font, fg='#563d2d', bg='white')
# search_entry.pack(side="right", padx=2, anchor=E)

# back_button = tk.Button(window, text="Back", bg='#563d2d', fg='white', font=button_font, command=exit_click, width=10)
# back_button.pack(side="bottom", anchor="se", padx=20, pady=10)


# # # Create a frame for the labels
# # labels_frame = tk.Frame(window, bg="white")
# # labels_frame.pack(side="right", padx=10, pady=10, anchor="ne")

# # # Create the labels for total books and total users inside the frame
# # total_books_label = tk.Label(labels_frame, text="Total Books: ", font=button_font, bg="white")
# # total_books_label.pack(side="top", anchor="ne", padx=10, pady=10)

# # total_users_label = tk.Label(labels_frame, text="Total Users: ", font=button_font, bg="white")
# # total_users_label.pack(side="top", anchor="ne", padx=10, pady=10)

# # # Function to update the total books and total users labels
# # def update_totals():
# #     # Retrieve the sum of quantities from the Books table
# #     cursor.execute("SELECT SUM(quantity) FROM Books")
# #     total_books = cursor.fetchone()[0]
# #     if total_books:
# #         total_books = int(total_books)
# #     else:
# #         total_books = 0

# #     # Retrieve the total number of user accounts from the user_account table
# #     cursor.execute("SELECT COUNT(*) FROM user_account")
# #     total_users = cursor.fetchone()[0]

# #     # Update the labels with the retrieved values
# #     total_books_label.config(text="Total Books: " + str(total_books))
# #     total_users_label.config(text="Total Users: " + str(total_users))
# # # Call the update_totals function initially to display the initial values
# # update_totals()

# # Function to generate and display the bar chart

# def generate_bar_chart():
#     # Fetch data from the UserHistory table
#     cursor.execute("SELECT transaction_type, COUNT(*) FROM UserHistory GROUP BY transaction_type")
#     results = cursor.fetchall()

#     # Separate the data into two lists: transaction types and counts
#     transaction_types = [result[0] for result in results]
#     counts = [result[1] for result in results]

#     # Create the bar chart with specified figure size
#     fig, ax = plt.subplots(figsize=(5, 4))  # Adjust the figure size as per your preference
#     ax.bar(transaction_types, counts)
#     ax.set_xlabel('Transaction Type')
#     ax.set_ylabel('Count')
#     ax.set_title('Transaction Types: Issued vs. Returned')

#     # Set the y-axis range from 0 to the maximum count + 1
#     ax.set_ylim(0, max(counts) + 1)

#     # Create a FigureCanvasTkAgg instance and embed the chart in the window
#     chart_canvas = FigureCanvasTkAgg(fig, master=window)
#     chart_canvas.draw()
#     # Adjust the position and padding as per your requirement
#     chart_canvas.get_tk_widget().pack(side="right", padx=0, pady=0, expand=True)

# # Call the function to generate and display the bar chart
# generate_bar_chart()

# # Table
# table_frame = tk.Frame(window, bg="#d3bbab")

# # Modify the table_frame widget's pack method parameters
# table_frame.pack(side="left", pady=18,padx=10, fill="both", expand=True, anchor="nw")

# columns = ("#", "Title", "Author", "Genre", "Quantity", "Status")
# table = ttk.Treeview(table_frame, columns=columns, show="headings")
# for col in columns:
#     table.heading(col, text=col)
#     table.column(col, width=70)
# table.pack(side="left", fill="both", expand=True)
# # Scrollbar
# scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
# scrollbar.pack(side="right", fill="y")
# table.configure(yscrollcommand=scrollbar.set)




# # Buttons
# buttons_frame = tk.Frame(window, bg="#d3bbab")
# buttons_frame.pack(side="left", padx=20)

# # add_button = tk.Button(buttons_frame, text="Add New", width=10,command=add_product)
# # add_button.pack(fill="x", padx=5, pady=10)

# # Populate the table with data from the database
# populate_table()
# window.protocol("WM_DELETE_WINDOW", sign_out)  # Bind exit_click to window close
# window.mainloop()
