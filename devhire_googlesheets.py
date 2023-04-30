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
    
    
    
print("\nWelcome To User Data Entry")
# Prompt for new user or exit
while True:
    choice = input("\nEnter '!' to exit or any other key to enter a new user: ")
    if choice == "!":
        break

    while True:
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        email = input("Enter your email: ")

        if not (first_name.isalpha() and last_name.isalpha()):
            print("Invalid name format. Please try again.")
            continue

        if not validate_email(email):
            print("Invalid email format. Please try again.")
            continue
    
        existing_emails = wks.col_values(3) #to check for a returning user and keeping new users unique
        #ashad this is the method you can use for retrieving data as 3rd coloumn is hardcoded for emails
        if email in existing_emails:
            print("Email already exists in the sheet. Please try again with a different email.")
            continue
        
        verification_code = gen_email_otp()
        send_otp_email(email,verification_code)
        
        start_time = time.time()
        while time.time() - start_time < 120:
            entered_otp = input("Enter the code sent to your email (within 2 minutes) : ")
            if entered_otp != verification_code:
                print("Verification Code Invalid or Expired, try again and if code not recieved check your mail SPAM")
                continue
            else:
                break
        break
    
    row = [first_name, last_name, email] #will insert in this order 
    wks.insert_row(row, index=2) #is hardcoded to insert at 2nd row always pushing others one row down
    #first row has titles
    print("User added successfully!")



