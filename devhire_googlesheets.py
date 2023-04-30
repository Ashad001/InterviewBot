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
def send_otp_email(email,verification_code):
    with open('login.txt', 'r') as f:
        lines = f.readlines()
        devhire_email = lines[0].strip()
        devhire_email_password = lines[1].strip()
    mail_content = MIMEMultipart("alternative")
    mail_content['Subject'] = 'DevHire One Time Verification'
    mail_content['From'] = devhire_email
    mail_content['To'] = email
    text = f"Your Verification Code For DevHire Signup Is : {verification_code}"
    #HTML content
    html = f"""
    <!DOCTYPE html>
    <html>
    <body>
        <!-- Logo section -->
        <div id="logo">
            <td style="background-color:white;">
                <img src="https://lh3.googleusercontent.com/drive-viewer/AFGJ81rxuocJq92t5lIyKSE51q-xBEsMu3ah0tJxlnpw_VHkmzZ3NSo1yqWIrd0EI8W3QvSJIIRZgwWx_dEHjVuRkZ7rQYixxw=s2560" alt="logo.png" height="250" width=auto style="padding-top: 1rem;">
            </td>
        </div>

        <!-- Main content -->
        <div class="content" style="align: left 1px; background: -webkit-linear-gradient(0deg,#39b1b2 ,#000000 100%);">
            <h1 style="font-size: 2.5em;">Verification Code</h1>
            <p style="font-size: 1.5em;">Please use the verification code below to sign in.</p>
            <br>
            <table>
                <tr>
                    <td>
                        <br>
                        <h1 strong style="font-size:3.5em; color:#ffffff;letter-spacing: 0.2em;">{verification_code} </h3>
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
    part1 = MIMEText(text ,'plain')
    part2 = MIMEText(html,'html')
    mail_content.attach(part1)
    mail_content.attach(part2)
    
    
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as server:
        server.login(devhire_email,devhire_email_password)
        server.send_message(mail_content)
    
def verify_user():
        verification_code = gen_email_otp()
        send_otp_email(email,verification_code)
            
        start_time = time.time()
        while time.time() - start_time < 1:
            entered_otp = input("Enter the code sent to your email (within 2 minutes) : ")
            if entered_otp != verification_code or time.time() - start_time > 1:
                print("Verification Code Invalid or Expired, try again and if code not recieved check your mail SPAM")
                break
            if entered_otp == verification_code:
                if time.time() - start_time > 1:
                    print("Verification Code Expired")
                    break
                break
            else:
                break
        

    
print("\nWelcome To User Data Entry")
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
        row_num = cell.row
        first_name = wks.cell(row_num,1).value
        score1 = wks.cell(row_num,4).value
        score2 = wks.cell(row_num,5).value
        score3 = wks.cell(row_num,6).value
        if verify_user():
            print(f"Welcome back {first_name}, You have signed in successfully\nHere are your scores from your last session\nSCORE 1: {score1}\nSCORE 2: {score2}\nSCORE 3: {score3}")
            break    
        else:
            while not verify_user():
                verify_user()


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
    print("User added successfully!")



