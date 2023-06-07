import gspread #for sheets
import random
from email.message import EmailMessage
import smtplib #for sending verification emails through python
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from flask import Flask, request, jsonify, render_template
from flask import session
from reportMailscript import send_mail
from flask_cors import CORS
import gspread
from Interivew import *

gc = gspread.service_account(filename='sheetAuth.json') #giving sheet access

wks = gc.open("devhire_Database").sheet1

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
    
def gen_email_otp():
    otp = str(random.randint(100000,999999))
    return otp    

def genOTP(first_name,last_name,email):
    existing_emails = wks.col_values(3) #to check for a returning user and keeping new users unique
    if email in existing_emails:
        return "742"
        # redirect(url_for('signuperror'))
    else:
        verification_code = gen_email_otp()
        send_otp_email(first_name,email,verification_code)
        return verification_code
        
def putScore(tone,und,ai,email):
    cell = wks.find(email)
    row_num = cell.row
    flag = ""
    try:
        wks.cell(row_num,4).value = tone
        wks.cell(row_num,5).value = und
        wks.cell(row_num,6).value = ai 
        flag = "Found" 
    except ValueError:
        flag = "Not Found"
    return flag
        
    
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

interviews = [None] * 100
app.secret_key = os.urandom(24)

@app.route("/")
def defaultPage():
    return render_template("signup2.html")

@app.route("/signup", methods=['GET'])
def signupPage():
    return render_template("signup2.html")

@app.route("/signin", methods=['GET'])
def signinPage():
    return render_template("signin2.html")

@app.route("/signinerror", methods=['GET'])
def signinErrorPage():
 return render_template("signinerror.html")

@app.route("/signuperror", methods=['GET'])
def signupErrorPage():
 return render_template("signuperror.html")

@app.route("/getOTP",methods=["POST","GET"])
def getOTPfunc():
    data = request.get_json()
    data = dict(data)
    ver = genOTP(data['first'],data['last'],data['email'])
    return ver

@app.route("/sendOTP",methods=["POST","GET"])
def sendOTPfunc():
    data = request.get_json()
    data = dict(data)
    ver = find_email(data['email'])
    return ver

@app.route("/enterinsheet",methods=["POST","GET"])
def sheetEntryfunc():
    data = request.get_json()
    data = dict(data)
    first_name,last_name,email = data['first'],data['last'],data['email']
    ver = jsonify({"first":first_name,"email":email})
    row = [first_name, last_name, email] #will insert in this order 
    wks.insert_row(row, index=2)
    return ver

@app.route('/get_values',methods=["POST","GET"])
def getValsfunc():
    data = request.get_json()
    cell = wks.find(data["email"])
    row_num = cell.row
    name = wks.cell(row_num,1).value 
    tone = wks.cell(row_num,4).value
    und = wks.cell(row_num,5).value 
    ai = wks.cell(row_num,6).value   
    
    # write a function to retrieve already exiting data from the Gsheets using the email that is stored in the data variable.
    values = jsonify({"tone":tone,"und":und,"ai":ai,"fname":name})
    return values   

@app.route('/scoreputter',methods=["POST","GET"])
def scorePutfunc():
    data = request.get_json()
    tone,und,ai,email = data['tone'],data['und'],data['AI'],data['email']
    print("\n",tone,und,ai,email,"\n")
    putScore(tone,und,ai,email)
    return None

@app.route("/interview", methods=['GET'])
def interviewer():
    return render_template("InterviewBot.html")

@app.route("/starter",methods=["POST","GET"])
def runner():
    global kkkk
    fname = str(request.json["fname"])
    interview_index = session.get('interview_index', None)
    kkkk = interview_index
    if interview_index is None:
        for i in range(len(interviews)):
            if interviews[i] is None:
                interview_temp = Interview(fname)
                interviews[i] = interview_temp
                interview_index = int(i)
                session['interview_index'] = interview_index # Store the interview index in the session
                break

    result = interviews[int(interview_index)].run(str(request.json["prompt"]))
    response = jsonify({"result":str(result[0])})
    response.headers.add('Access-Control-Allow-Origin', 'https://devday23.tech')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response

@app.route("/receive-data",methods=["POST","GET"])
def receive_data():
    interview_index = session.get('interview_index', None) # Get the interview index from the session
    data = request.json
    result = interviews[int(interview_index)].run(str(data))
    print(result)
    scores = result[2] # Scores: [Tone, Understanding, Bot]
    flag = 0
    if result[1] == 0:
    #     with app.test_request_context('/stopper_yay', method=["POST", "GET"]):
    #         return app.stopper1()
        flag=1
        scores = scores
        report = interviews[interview_index].get_report_data()
        send_mail("ashad001sp@gmail.com", scores=scores, report=report)
        response = jsonify({"ans":"The Interview has ended, please check your email for the detailed report of this session.\nThank you for speaking with us. To have another session please login again.","score":scores, "flag":flag})
        interviews[interview_index] = None
        session.pop('interview_index', None) # Remove the interview index from the session
        return response
    response = {"ans":result[0],"score":scores, "flag":flag}
    return jsonify(response)

@app.route('/end-session')
def end_session():
  interview_index = session.get('interview_index', None)
  if interview_index is not None:
    interviews[interview_index] = None
    session.pop('interview_index', None)
  return "Session ended due to inactivity please restart"

@app.route('/stopper_yay', methods=["POST", "GET"])
def stopper1():
    data = str(request.json['prompt'])
    email = str(request.json['email'])
    interview_index = session.get('interview_index', None)
    result = interviews[int(interview_index)].run(str(data))
    scores = result[2]
    flag = 1   
    report = interviews[int(interview_index)].get_report_data()
    answer = "Please complete the interview to get detailed report and analysis of your interview\nThankyou!"
    if report != -1:
        send_mail(email, scores=scores, report=report)
        answer = "The Interview has ended, please check your email for the detailed report of this session.\nThank you for speaking with us. To have another session please login again."
    response = jsonify({"ans": answer,"score":scores, "flag":flag})
    interviews[int(interview_index)] = None
    session.pop('interview_index', None)
    return response

if __name__ == "__main__":
    app.run()
