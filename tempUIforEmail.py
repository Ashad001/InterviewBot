# pip install tk
import tkinter as tk
from tkinter import messagebox
import gspread #for sheets
import re #for string verification such as email and name formats
import random
from email.message import EmailMessage
import smtplib
import time
import ssl

gc = gspread.service_account(filename='sheetAuth.json') #giving sheet access
wks = gc.open("devhire_Database").sheet1

def validate_email(email):
    pattern = r'^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$'
    return re.match(pattern, email)

def validate_name(name):
    pattern = r'^[a-zA-Z]+$'
    return re.match(pattern, name)

def gen_email_otp():
    otp = str(random.randint(100000,999999))
    return otp



context = ssl.create_default_context() 
def send_otp_email(email,verification_code):
    with open('login.txt', 'r') as f:
        lines = f.readlines()
        devhire_email = lines[0].strip()
        devhire_email_password = lines[1].strip()

    mail_content = EmailMessage()
    mail_content.set_content(f"Your Verification Code For DevHire Signup Is : {verification_code}")
    mail_content['Subject'] = 'DevHire One Time Verification'
    mail_content['From'] = devhire_email
    mail_content['To'] = email
    
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as server:
        server.login(devhire_email,devhire_email_password)
        server.send_message(mail_content)

def verify_email():
    email = email_entry.get()

    if not validate_email(email):
        messagebox.showerror("Error", "Invalid email format. Please try again.")
        return

    existing_emails = wks.col_values(3)
    if email in existing_emails:
        messagebox.showerror("Error", "Email already exists in the sheet. Please try again with a different email.")
        return

    verification_code = gen_email_otp()
    send_otp_email(email, verification_code)

    # Wait for OTP to be entered
    otp_label.pack()
    otp_entry.pack()
    add_user_button.config(state='disabled')
    start_time = time.time()
    while time.time() - start_time < 120:
        entered_otp = otp_entry.get()
        if entered_otp == verification_code:
            messagebox.showinfo("Success", "Email verified!")
            otp_label.pack_forget()
            otp_entry.pack_forget()
            add_user_button.config(state='normal')
            break
        elif entered_otp:
            messagebox.showerror("Error", "Verification Code Invalid or Expired, try again and if code not recieved check your mail SPAM")


def add_user():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()

    if not (first_name.isalpha() and last_name.isalpha()):
        messagebox.showerror("Error", "Invalid name format. Please try again.")
        return

    if not validate_email(email):
        messagebox.showerror("Error", "Invalid email format. Please try again.")
        return

    existing_emails = wks.col_values(3)
    if email in existing_emails:
        messagebox.showerror("Error", "Email already exists in the sheet. Please try again with a different email.")
        return

    verification_code = gen_email_otp()
    send_otp_email(email,verification_code)

    # Wait for OTP to be entered
    otp_label.pack()
    otp_entry.pack()
    add_user_button.config(state='disabled')
    start_time = time.time()
    while time.time() - start_time < 120:
        entered_otp = otp_entry.get()
        if entered_otp == verification_code:
            row = [first_name, last_name, email]
            wks.insert_row(row, index=2)
            messagebox.showinfo("Success", "User added successfully!")
            otp_label.pack_forget()
            otp_entry.pack_forget()
            add_user_button.config(state='normal')
            break
        elif entered_otp:
            messagebox.showerror("Error", "Verification Code Invalid or Expired, try again and if code not recieved check your mail SPAM")

def exit_program():
    root.destroy()



root = tk.Tk()
root.title("DevHire User Data Entry")

# First Name
first_name_label = tk.Label(root, text="First Name:")
first_name_label.pack()
first_name_entry = tk.Entry(root)
first_name_entry.pack()

# Last Name
last_name_label = tk.Label(root, text="Last Name:")
last_name_label.pack()
last_name_entry = tk.Entry(root)
last_name_entry.pack()

# Email
email_label = tk.Label(root, text="Email:")
email_label.pack()
email_entry = tk.Entry(root)
email_entry.pack()

# Verify Email Button
verify_email_button = tk.Button(root, text="Verify Email", command=verify_email)
verify_email_button.pack()

# OTP
otp_label = tk.Label(root, text="OTP:")
otp_label.pack()
otp_entry = tk.Entry(root)
otp_entry.pack()

# Add User Button
add_user_button = tk.Button(root, text="Add User", command=add_user, state=tk.DISABLED)
add_user_button.pack()

# Exit Button
exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.pack()

root.mainloop()
