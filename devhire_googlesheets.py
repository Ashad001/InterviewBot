import gspread #for sheets
import re #for string verification such as email and name formats
import random
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import time
import ssl
gc = gspread.service_account(filename='E:/fourth sem/Shit/InterviewBot/sheetAuth.json') #giving sheet access
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
def send_otp_email(name, email,verification_code):
    with open('E:/fourth sem/Shit/InterviewBot/login.txt', 'r') as f:
        lines = f.readlines()
        devhire_email = lines[0].strip()
        devhire_email_password = lines[1].strip()

    smtp_server = "smtp.gmail.com"
    message = MIMEMultipart("alternative")
    message['Subject'] = f"OTP for DevHire - {name.capitalize()}"
    message['From'] = devhire_email
    message['To'] = email
    
    text = f"Greeting {name}, Here is your OTP for DevHire {verification_code}"
    #HTML content
    html = f"""
    <!DOCTYPE html>
    <html>
    <body>
        <!-- Logo section -->
        <div id="logo">
            <td style="background-color:white;">
                <img src="./email_logo.png" height="250" width=auto style="padding-top: 1rem;">
            </td>
        </div>

        <!-- Main content -->
        <div class="content" style="align: left 1px; background: -webkit-linear-gradient(0deg,#39b1b2 ,#000000 100%);">
            <h1 style="font-size: 2.5em;"> {verification_code} </h1>
            <p style="font-size: 1.5em;">Please use the verification code below to sign in.</p>
            <br>
            <table>
                <tr>
                    <td>
                        <br>
                        <h1 strong style="font-size:3.5em; color:#ffffff;letter-spacing: 0.2em;">847117</h3>
                    </td>
                </tr>
            </table>
            <p style="font-size:1.5em" ;>If you didn't request this, you can ignore this email.</p>
            <br>
            <p strong style="font-size:1.5em" ;>Thanks,</p>
            <p style="font-size:1.5em" ;>The DevHire Team</p>
            <br><br><br>
            <h2>Contact Us</h2>
            <p>For any questions or inquiries, please send us an email at <a
                    href="mailto:devhire.info@gmail.com">info@devday.com</a>.</p>
        </div>
    </body>

    </html>
        
    """

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    
    message.attach(part1)
    message.attach(part2)
    
    context = ssl.create_default_context()
    
    try:
        server = smtplib.SMTP_SSL(smtp_server, 465, context=context)
        server.login(devhire_email, devhire_email_password)
        server.sendmail(devhire_email, email, message.as_string())
        print('Email sent!')
    except Exception as e:
        print(f"Something went wrong... {e}")
            

   
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
        send_otp_email(first_name, email,verification_code)
        
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



