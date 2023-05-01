import gspread #for sheets
import re #for string verification such as email and name formats
import random
from email.message import EmailMessage
import smtplib #for sending verification emails through python
import time
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
def send_otp_email(first_name,email,verification_code):
    with open('login.txt', 'r') as f:
        lines = f.readlines()
        devhire_email = lines[0].strip()
        devhire_email_password = lines[1].strip()
    mail_content = MIMEMultipart("alternative")
    mail_content['Subject'] = 'DevHire One Time Verification'
    mail_content['From'] = devhire_email
    mail_content['To'] = email
    text = f"Your Verification Code For DevHire Signup Is : {verification_code}"
    #HTML content for email template
    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Verification Email</title>
        </head>
        <body>
            <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
                <div style="margin:50px auto;width:80%;padding:20px 0">
                    <div style="border-bottom:5px solid #eee">
                        <img src="https://lh3.googleusercontent.com/drive-viewer/AFGJ81rxuocJq92t5lIyKSE51q-xBEsMu3ah0tJxlnpw_VHkmzZ3NSo1yqWIrd0EI8W3QvSJIIRZgwWx_dEHjVuRkZ7rQYixxw=s2560" alt="logo.png"  style="display:block; margin:auto;" height="300" width=auto>
                    </div >
                    <div style="color:white; text-align:center; background: -webkit-linear-gradient(0deg,#39b1b2 ,#000000 100%);">
                        <p style="font-size:15px;color: white;">Hello {first_name},</p>
                        <p>Welcome To DevHire. Use this code to complete your accounts verification process.</p>
                        <p>Remember, Never share this code with anyone.</p>
                        <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{verification_code}</h2>
                        <p style="font-size:15px;">Regards,<br />Team DevHire</p>
                    </div>
                    <hr style="border:none;border-top:5px solid #eee" />
                    <div style="float:left;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
                        <p>Contact Us</p>
                        <p><a href="mailto:devhirecontact@gmail.com">devhirecontact@gmail.com</a>.</p>
                    </div>
                </div>
            </div>
        </body>
    </html>
        
    """
    part1 = MIMEText(text ,'plain')
    part2 = MIMEText(html,'html')
    mail_content.attach(part1)
    mail_content.attach(part2)
    
    
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as server:
        server.login(devhire_email,devhire_email_password)
        server.send_message(mail_content)
    
def verify_user():
        verification_code = gen_email_otp()
        send_otp_email(first_name,email,verification_code)
            
        start_time = time.time()
        while time.time() - start_time < 120:
            entered_otp = input("Enter the code sent to your email (within 2 minutes) : ")
            if entered_otp != verification_code:
                print("Verification Code Invalid or Expired, try again and if code not recieved check your mail SPAM")
                continue
            else:
                break
        

    
print("\nWelcome To DevHire User Account")
# Prompt for new user,returning user or exit
while True:
    choice = input("\n Enter '!' to exit \n Enter 'n' to enter a new user\n Enter 'r' if you already have an account\n ")
    if choice == "!":
        break
    
    if choice == "r" or choice == "R":
        email = input("Enter your registered email: ")
        if not validate_email(email):
                print("Invalid email format. Please try again.")
                continue
        cell = wks.find(email)

        if cell is None:
            print("\nThis Email is not registered with DevHire.\n")
        else:
            row_num = cell.row
            first_name = wks.cell(row_num,1).value
            Tone = wks.cell(row_num,4).value
            Understanding = wks.cell(row_num,5).value
            Ai_Analysis = wks.cell(row_num,6).value
            verify_user()
            print(f"Welcome back {first_name}, You have signed in successfully\nHere are your scores from your last session\nTone Score: {Tone}\nUnderstanding Score: {Understanding}\nAi Analysis: {Ai_Analysis}")
        break

    if choice == "n" or choice == "N":
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
                print("This Email is already registered. Please try again with a different email or Sign in as a returning user.")
                continue
            verify_user()
            break
    
    row = [first_name, last_name, email] #will insert in this order 
    wks.insert_row(row, index=2) #is hardcoded to insert at 2nd row always pushing others one row down
    #first row has titles
    print("Signup Successful")



