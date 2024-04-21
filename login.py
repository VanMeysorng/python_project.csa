import tkinter as tk
from tkinter import ttk, messagebox, Frame, Button, Label, Entry
from PIL import Image, ImageTk
import mysql.connector
import subprocess

# Global variables
login_attempts = 0
wait_time = 30
user_id = None


def login_handler():
    validate_login(username_entry.get(), password_entry.get())

# Add other functions here
def validate_login(username, password):
    global login_attempts, wait_time, user_id

    try:
        conn = mysql.connector.connect(
            user="root",
            password="ms123456",
            host="localhost",
            database="Library"
        )

        cursor = conn.cursor()

        if username == "admin" and password == "1234":
            root.destroy()
            messagebox.showinfo("Success", "Welcome, Admin!")
            subprocess.run(['python', 'admin_bookmanagement.py'])
            login_attempts = 0
            wait_time = 30
        else:
            sql = "SELECT * FROM user_account WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))

            result = cursor.fetchone()

            if result:
                user_id = result[0]
                with open('user_id.txt', 'w') as file:
                    file.write(str(user_id))

                update_logged_in_status(cursor, user_id, 1)
                conn.commit()

                root.destroy()
                messagebox.showinfo("Success", "Welcome, "+username)
                subprocess.run(['python', 'user_book.py'])
                login_attempts = 0
                wait_time = 30
            else:
                login_attempts += 1
                if login_attempts >= 5:
                    wait_time_remaining = wait_time
                    def close_messagebox():
                        messagebox.showerror("Login Failed", f"Too many failed attempts. Please try again after {wait_time_remaining} seconds.")
                        login_attempts = 0
                    root.after(wait_time * 1000, close_messagebox)
                    wait_time += 30
                else:
                    messagebox.showerror("Login Failed", "Invalid username or password")
    
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"An error occurred: {str(err)}")

def update_logged_in_status(cursor, user_id, status):
    update_sql = "UPDATE user_account SET logged_in = %s WHERE id = %s"
    cursor.execute(update_sql, (status, user_id))

def sign_out():
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
            update_logged_in_status(cursor, user_id, 0)
            conn.commit()
            user_id = None

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {str(err)}")
    root.destroy()

def on_enter_usesrname(e):
    username_entry.delete(0, 'end')

def on_leave_username(e):
    name = username_entry.get()
    if name == '':
        username_entry.insert(0, 'Username')

def on_enter_password(e):
    if password_entry.get() == 'Password':
        password_entry.delete(0, 'end')
        password_entry.config(show="*")

def on_leave_password(e):
    if password_entry.get() == '':
        password_entry.config(show="")
        password_entry.insert(0, 'Password')

def sign_up_handler():
    # Add code to navigate to the login.py file
    root.destroy()
    subprocess.run(["python", "signup.py"])

root = tk.Tk()
root.title("Library Management System")
root.geometry("960x610")
root.resizable(False, False)

img = Image.open('coverbg.png')
img = img.resize((960, 610))
img = ImageTk.PhotoImage(img)

label = Label(root, image=img, bg="white")
label.pack()

frame = Frame(root, width=370, height=370, bg='white')
frame.place(x=520, y=105)

heading = Label(frame, text='Log In', anchor='center', fg='#5C3C2B', bg='white', font=('Lato', 23, 'bold'))
heading.place(x=135, y=40)

login_attempts = 0
wait_time = 30
user_id = None

username_entry = Entry(frame, width=25, fg='black', bg='white', font=('Lato', 11), bd=0, highlightthickness=0)
username_entry.place(x=35, y=115)
username_entry.insert(0, 'Username')
username_entry.bind('<FocusIn>', on_enter_usesrname)
username_entry.bind('<FocusOut>', on_leave_username)

tk.Frame(frame, width=295, height=2, bg='#5C3C2B').place(x=35, y=135)

password_entry = Entry(frame, fg='black', border=0, bg='white', highlightbackground='white', highlightthickness=0, font=('Lato', 11))
password_entry.place(x=35, y=155)  # Correct placement for the password entry
password_entry.insert(0, 'Password')
password_entry.bind('<FocusIn>', on_enter_password)
password_entry.bind('<FocusOut>', on_leave_password)

tk.Frame(frame, width=295, height=2, bg='#5C3C2B').place(x=35, y=175)


Button(frame, width=9, pady=7, text='Log In', fg='white', bg='#5C3C2B', command=login_handler).place(x=140, y=220)

label1 = Label(frame, text="Doesn't have an account yet?", fg='Black', bg='white', font=('Ariel', 10))
label1.place(x=66, y=300)

Button(frame, width=6, pady=7, text='Sign Up', bg='white', fg='#5C3C2B',borderwidth=0, font=('Ariel', 10),command=sign_up_handler).place(x=240, y=293)

register_error_label = Label(frame, text="", fg='red', font=('Ariel', 12))
register_error_label.place(x=165, y=410)

root.mainloop()
