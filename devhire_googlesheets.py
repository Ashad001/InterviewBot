import gspread #for sheets
import re #for string verification such as email and name formats
import random
from email.message import EmailMessage
import smtplib #for sending verification emails through python
import time
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, jsonify

gc = gspread.service_account(filename='sheetAuth.json') #giving sheet access
wks = gc.open("devhire_Database").sheet1

# def validate_email(email):
#     pattern = r'^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$'
#     return re.match(pattern, email)

# def validate_name(name):
#     pattern = r'^[a-zA-Z]+$'
#     return re.match(pattern, name)

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
    # HTML content for email template
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
    
def genOTP(first_name,last_name,email):
    existing_emails = wks.col_values(3) #to check for a returning user and keeping new users unique
    if email in existing_emails:
        return "742"
        # redirect(url_for('signuperror'))
    else:
        verification_code = gen_email_otp()
        send_otp_email(first_name,email,verification_code)
        return verification_code
        

    
def find_email(email):
    cell = wks.find(email)

    if cell is None:
        return "742"

    else:
        verification_code = gen_email_otp()
        row_num = cell.row
        first_name = wks.cell(row_num,1).value
        Tone = wks.cell(row_num,4).value
        Understanding = wks.cell(row_num,5).value
        Ai_Analysis = wks.cell(row_num,6).value
        send_otp_email(first_name,email,verification_code)
        #print(Tone,Understanding,Ai_Analysis,first_name)
        return verification_code



app = Flask(__name__,template_folder="templates")

@app.route("/")
def aut():
    return render_template("signup2.html")

@app.route("/signup")
def aut5():
    return render_template("signup2.html")

@app.route("/signin")
def aut1():
    return render_template("signin2.html")

@app.route("/signinerror")
def aut2():
 return render_template("signinerror.html")

@app.route("/signuperror")
def aut3():
 return render_template("signuperror.html")

@app.route("/getOTP",methods=["POST","GET"])
def receive_data():
    data = request.get_json()
    data = dict(data)
    ver = genOTP(data['first'],data['last'],data['email'])
    return ver

@app.route("/sendOTP",methods=["POST","GET"])
def receive2_data():
    data = request.get_json()
    data = dict(data)
    ver = find_email(data['email'])
    return ver

@app.route("/enterinsheet",methods=["POST","GET"])
def receive_verified_data():
    data = request.get_json()
    data = dict(data)
    first_name,last_name,email = data['first'],data['last'],data['email']
    ver = jsonify({"first":first_name,"last":last_name,"email":email})
    row = [first_name, last_name, email] #will insert in this order 
    wks.insert_row(row, index=2)
    return ver

@app.route('/get_values')
def get_values():
    data = request.get_json()
    data = dict(data)
    values = ([data['first_name'],data['Tone'],data['Understanding'],data['Ai_Analysis']])
    return jsonify(values)    


if __name__ == "__main__":
    app.run()
