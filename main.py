import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import time
import subprocess

def create_account_handler():
    create_account(full_name_entry, email_entry, register_username_entry, register_password_entry, confirm_password_entry, register_error_label)

def login_handler():
    validate_login(username_entry, password_entry)

# Global variables
login_attempts = 0
wait_time = 30
user_id = None  # Store the logged-in user ID

def show_error_message(message):
    messagebox.showerror("Login Failed", message)

def validate_login(username_entry, password_entry):
    global login_attempts, wait_time, user_id

    username = username_entry.get()
    password = password_entry.get()

    try:
        conn = mysql.connector.connect(
            user="root",
            password="ms123456",
            host="localhost",
            database="Library"
        )

        cursor = conn.cursor()

        # Validate admin login
        if username == "admin" and password == "1234":
            messagebox.showinfo("Login Successful", "Welcome, admin!")
            root.destroy()
            subprocess.run(['python', 'admin_bookmanagement.py'])
            login_attempts = 0  # Reset login attempts upon successful login
            wait_time = 30  # Reset wait time
        else:
            # Query the user_account table for the entered username and password
            sql = "SELECT * FROM user_account WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))

            result = cursor.fetchone()

            if result:
                user_id = result[0]  # Store the logged-in user ID
                # Storing the user_id in a file
                with open('user_id.txt', 'w') as file:
                    file.write(str(user_id))

                update_logged_in_status(cursor, user_id, 1)  # Set logged_in status to 1 for the logged-in user
                conn.commit()

                messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                root.destroy()
                subprocess.run(['python', 'user_book.py'])
                login_attempts = 0  # Reset login attempts upon successful login
                wait_time = 30  # Reset wait time
            else:
                login_attempts += 1
                if login_attempts >= 5:
                    wait_time_remaining = wait_time
                    def close_messagebox():
                        messagebox.showerror("Login Failed", f"Too many failed attempts. Please try again after {wait_time_remaining} seconds.")
                        login_attempts = 0  # Reset login attempts after the wait period
                    root.after(wait_time * 1000, close_messagebox)
                    wait_time += 30  # Increase wait time by 30 seconds for the next attempt
                else:
                    messagebox.showerror("Login Failed", "Invalid username or password")
    
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"An error occurred: {str(err)}")

def update_logged_in_status(cursor, user_id, status):
    update_sql = "UPDATE user_account SET logged_in = %s WHERE id = %s"
    cursor.execute(update_sql, (status, user_id))

def sign_out():
    # Retrieving the user_id from the file
    with open('user_id.txt', 'r') as file:
        user_id = int(file.read())

    if user_id:
        try:
            conn = mysql.connector.connect(
                user="root",
                password="ms123456",
                host="localhost",
                database="Library"
            )

            cursor = conn.cursor()
            update_logged_in_status(cursor, user_id, 0)  # Set logged_in status to 0 for the logged-out user
            conn.commit()
            user_id = None  # Reset the user ID

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {str(err)}")
    root.destroy()  # Close the application

def switch_to_register():
    # Hide login frame, show registration frame
    login_frame.pack_forget()
    register_frame.pack()

def go_back():
    # Hide registration frame, show login frame
    register_frame.pack_forget()
    login_frame.pack()
    
def create_account(full_name_entry, email_entry, register_username_entry, register_password_entry, confirm_password_entry, register_error_label):
    full_name = full_name_entry.get()
    email = email_entry.get()
    username = register_username_entry.get()
    password = register_password_entry.get()
    confirm_password = confirm_password_entry.get()

    # Check if any of the required fields are empty
    if not full_name or not email or not username or not password or not confirm_password:
        register_error_label.config(text="Please fill in all the required fields.", foreground="red")
        return

    try:
        conn = mysql.connector.connect(
            user="root",
            password="ms123456",
            host="localhost",
            database="Library"
        )

        cursor = conn.cursor()

        if password != confirm_password:
            register_error_label.config(text="Passwords do not match. Please enter the same password.", foreground="red")
        else:
            sql = "INSERT INTO user_account (full_name, email, username, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (full_name, email, username, password))

            conn.commit()
            conn.close()

            register_error_label.config(text="Account created successfully!", foreground="green")
            messagebox.showinfo("Success", "Account created successfully!")

            # Clear input fields
            full_name_entry.delete(0, 'end')
            email_entry.delete(0, 'end')
            register_username_entry.delete(0, 'end')
            register_password_entry.delete(0, 'end')
            confirm_password_entry.delete(0, 'end')

    except mysql.connector.Error as err:
        register_error_label.config(text=f"Error creating account: {str(err)}", foreground="red")

root = tk.Tk()
root.title("Library Management System")
root.configure(bg="beige")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - 1000) / 2
y = (screen_height - 700) / 2 - 100

root.geometry("1000x700".format(int(x), int(y)))
root.resizable(False, False)

container = ttk.Frame(root)
container.pack(expand=True, fill="both")

style = ttk.Style()
style.theme_use('clam')
style.configure('TEntry', fieldbackground="beige")
style.configure('TLabel', background="beige")
style.configure('TButton', background="beige")
style.configure('TFrame', background="beige")

style = ttk.Style()
style.configure('Blue.TButton', background='lightblue')
style.configure('Red.TButton', background='lightcoral')

# Create login frame
login_frame = ttk.Frame(container, padding=(20, 20))

# Create registration frame
register_frame = ttk.Frame(container, padding=(20, 20))

# Login Form
logo_image = Image.open("logo.png")
logo_image = logo_image.resize((150, 150))
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = ttk.Label(login_frame, image=logo_photo, background="beige")
logo_label.grid(row=0, column=0, pady=(10, 20), sticky="we")

system_label = ttk.Label(login_frame, text="Library Management System", font=("Arial", 30, 'bold'), background="beige")
system_label.grid(row=0, column=1, columnspan=2, pady=(10, 20), padx=(10, 0), sticky="w")

instruction_label = ttk.Label(login_frame, text="Please fill in your information to access the system.", font=("Arial", 12), anchor="center", background="beige")
instruction_label.grid(row=1, column=0, columnspan=3, pady=(0, 10), sticky="we")

username_label = ttk.Label(login_frame, text="Username:", font=("Arial, 20"), background="beige")
username_label.grid(row=2, column=0, padx=10, pady=20, sticky="e")

password_label = ttk.Label(login_frame, text="Password:", font=("Arial, 20"), background="beige")
password_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

username_entry = ttk.Entry(login_frame)
username_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="we")
username_entry.focus_set()

password_entry = ttk.Entry(login_frame, show="*")
password_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="we")

login_button = ttk.Button(login_frame, text="Login", command=login_handler, style='Blue.TButton')
login_button.grid(row=4, column=1, pady=20)

# Registration Form
welcome_label = ttk.Label(register_frame, text="Welcome", font=("Arial", 36))
welcome_label.grid(row=0, column=0, columnspan=2, pady=10)

instruction_label = ttk.Label(register_frame, text="Enter your details below to create an account", font=("Arial", 18), foreground="#ae1d1d")
instruction_label.grid(row=1, column=0, columnspan=2, pady=10)

full_name_label = ttk.Label(register_frame, text="Full Name:", width=20)
full_name_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
full_name_entry = ttk.Entry(register_frame)
full_name_entry.grid(row=2, column=1, padx=5, pady=5)

email_label = ttk.Label(register_frame, text="Email:", width=20)
email_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
email_entry = ttk.Entry(register_frame)
email_entry.grid(row=3, column=1, padx=5, pady=5)

register_username_label = ttk.Label(register_frame, text="Username:", width=20)
register_username_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
register_username_entry = ttk.Entry(register_frame)
register_username_entry.grid(row=4, column=1, padx=5, pady=5)

register_password_label = ttk.Label(register_frame, text="Password:", width=20)
register_password_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
register_password_entry = ttk.Entry(register_frame, show="*")
register_password_entry.grid(row=5, column=1, padx=5, pady=5)

confirm_password_label = ttk.Label(register_frame, text="Confirm Password:", width=20)
confirm_password_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
confirm_password_entry = ttk.Entry(register_frame, show="*")
confirm_password_entry.grid(row=6, column=1, padx=5, pady=5)

register_error_label = ttk.Label(register_frame, text="", foreground="red")
register_error_label.grid(row=7, column=0, columnspan=2, pady=5)

create_button = ttk.Button(register_frame, text="Create Account", command=create_account_handler, style='Blue.TButton')
create_button.grid(row=8, column=0, pady=10)

go_back_button = ttk.Button(register_frame, text="Go Back", style='Red.TButton', command=go_back)
go_back_button.grid(row=8, column=1, pady=10)

# Place both frames in the container
login_frame.pack()
register_frame.pack_forget()

# Create the Register button to switch to the registration form
register_button = ttk.Button(login_frame, text="Register", command=switch_to_register, style='Red.TButton')
register_button.grid(row=4, column=2, pady=20, sticky="w")
root.protocol("WM_DELETE_WINDOW", sign_out)  # Bind exit_click to window close
root.mainloop()
