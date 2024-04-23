import tkinter as tk
from tkinter import ttk, messagebox, Frame, Button, Label, Entry
from PIL import Image, ImageTk
import mysql.connector
import subprocess

# Global variables
login_attempts = 0
wait_time = 30
user_id = None

def create_account_handler():
    create_account(
        full_name_entry, 
        email_entry, 
        register_username_entry, 
        register_password_entry, 
        confirm_password_entry, 
        register_error_label
    )

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
            password="Chetra1234",
            host="localhost",
            database="Library"
        )

        cursor = conn.cursor()

        if password != confirm_password:
            register_error_label.config(text="Passwords do not match.", foreground="red")
        else:
            # Update the SQL query to handle all input fields
            sql = "INSERT INTO user_account (full_name, email, username, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (full_name, email, username, password))

            conn.commit()
            conn.close()

            register_error_label.config(text="Account created successfully!", foreground="green")
            messagebox.showinfo("Success", "Account created successfully!")

            # Clear entry
        full_name_entry.delete(0, 'end')
        full_name_entry.insert(0, 'Full Name')

        email_entry.delete(0, 'end')
        email_entry.insert(0, 'Email')

        register_username_entry.delete(0, 'end')
        register_username_entry.insert(0, 'Username')

        register_password_entry.delete(0, 'end')
        register_password_entry.insert(0, 'Password')  # Set the value to "Password"

        confirm_password_entry.delete(0, 'end')
        confirm_password_entry.insert(0, 'Confirm Password') 


    except mysql.connector.Error as err:
        register_error_label.config(text=f"Error creating account: {str(err)}", foreground="red")


def on_enter_fullname(e):
    full_name_entry.delete(0, 'end')

def on_leave_fullname(e):
    name = full_name_entry.get()
    if name == '':
        full_name_entry.insert(0, 'Full Name')

def on_enter_email(e):
    email_entry.delete(0, 'end')

def on_leave_email(e):
    name = email_entry.get()
    if name == '':
        email_entry.insert(0, 'Email')

def on_enter_username(e):
    register_username_entry.delete(0, 'end')

def on_leave_username(e):
    name = register_username_entry.get()
    if name == '':
        register_username_entry.insert(0, 'Username')

def on_enter_password(e):
    if register_password_entry.get() == 'Password':
        register_password_entry.delete(0, 'end')
    register_password_entry.config(show="")

def on_leave_password(e):
    if register_password_entry.get() == '':
        register_password_entry.config(show="")
        register_password_entry.insert(0, 'Password')

def on_enter_confim_password(e):
    if confirm_password_entry.get() == 'Confirm Password':
        confirm_password_entry.delete(0, 'end')
        confirm_password_entry.config(show="")

def on_leave_confirm_password(e):
    if confirm_password_entry.get() == '':
        confirm_password_entry.config(show="")
        confirm_password_entry.insert(0, 'Confirm Password')

def log_in_handler():
    # Add code to navigate to the login.py file
    root.destroy()
    subprocess.run(["python", "login.py"])

root = tk.Tk()
root.title("Library Management System")
root.geometry("960x610")
root.resizable(False, False)

img = Image.open('coverbg.png')
img = img.resize((960, 610))
img = ImageTk.PhotoImage(img)

label = Label(root, image=img, bg="white")
label.pack()

frame = Frame(root, width=400, height=480, bg='white')
frame.place(x=505, y=55)

heading = Label(frame, text='Sign Up', anchor='center', fg='#5C3C2B', bg='white', font=('Lato', 23, 'bold'))
heading.place(x=147, y=25)

login_attempts = 0
wait_time = 30
user_id = None

full_name_entry = Entry(frame, width=25, fg='black', bg='white', font=('Lato', 11), bd=0, highlightthickness=0)
full_name_entry.place(x=35, y=87)
full_name_entry.insert(0, 'Full Name')
full_name_entry.bind('<FocusIn>', on_enter_fullname)
full_name_entry.bind('<FocusOut>', on_leave_fullname)

tk.Frame(frame, width=295, height=2, bg='#5C3C2B').place(x=35, y=112)

email_entry = Entry(frame, width=25, fg='black', bg='White', font=('Lato', 11), bd=0, highlightthickness=0)
email_entry.place(x=35, y=137)
email_entry.insert(0, 'Email')
email_entry.bind('<FocusIn>', on_enter_email)
email_entry.bind('<FocusOut>', on_leave_email)

tk.Frame(frame, width=295, height=2, bg='#5C3C2B').place(x=35, y=162)

register_username_entry = Entry(frame, width=25, fg='black', bg='White', font=('Lato', 11), bd=0, highlightthickness=0)
register_username_entry.place(x=35, y=187)
register_username_entry.insert(0, 'Username')
register_username_entry.bind('<FocusIn>', on_enter_username)
register_username_entry.bind('<FocusOut>', on_leave_username)

tk.Frame(frame, width=295, height=2, bg='#5C3C2B').place(x=35, y=212)

register_password_entry = Entry(frame, width=25, fg='black', bg='White', font=('Lato', 11), bd=0, highlightthickness=0)
register_password_entry.place(x=35, y=237)
register_password_entry.insert(0, 'Password')
register_password_entry.bind('<FocusIn>', on_enter_password)
register_password_entry.bind('<FocusOut>', on_leave_password)

tk.Frame(frame, width=295, height=2, bg='#5C3C2B').place(x=35, y=262)

confirm_password_entry = Entry(frame, width=25, fg='black', bg='White', font=('Lato', 11), bd=0, highlightthickness=0)
confirm_password_entry.place(x=35, y=287)
confirm_password_entry.insert(0, 'Confirm Password')
confirm_password_entry.bind('<FocusIn>', on_enter_confim_password)
confirm_password_entry.bind('<FocusOut>', on_leave_confirm_password)

tk.Frame(frame, width=295, height=2, bg='#5C3C2B').place(x=35, y=312)

Button(frame, width=9, pady=7, text='Sign Up', fg='white', bg='#5C3C2B', command=create_account_handler).place(x=155, y=340)

label1 = Label(frame, text="Doesn't have an account yet?", fg='Black', bg='white', font=('Ariel', 10))
label1.place(x=72, y=393)

Button(frame, width=6, pady=7, text='Log In', bg='white', fg='#5C3C2B', borderwidth=0, font= ('Ariel', 10),command=log_in_handler).place(x=245, y=385)

register_error_label = Label(frame, text="", fg='red', bg='white', font=('Ariel', 10))
register_error_label.place(x=108, y=418)

root.mainloop()
