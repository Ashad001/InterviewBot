import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re



def send_mail(recievermail, scores, report):
    port = 465  # For SSL
    receiver_email = recievermail
    # read mail from file
    with open("readmail.txt") as f:
        sender_email = f.read()
    # password read from file
    with open("password.txt") as f:
        password = f.read()
    
    
    smtp_server = "smtp.gmail.com"
    scores = scores
    report = report
    message = MIMEMultipart("alternative")
    message["Subject"] = "Score and Report"
    message["From"] = sender_email  
    message["To"] = receiver_email
    
    formatreport = re.split(r'\r?\n|\r|\n|(\w+):', report)
    
    report = " "
    for line in formatreport:
        if line is not None:
            report = report + line + '<br>'
    
    text = f"Hi,\n\nHere are your scores\n Score By Tone: {scores[0]} / 10.0\n Score by Question Understanding {scores[1]} / 10.0\n Score By Bot: {scores[2]} \ 10.0.\n\n{report}"
    # HTML content
    html = f"""
    <html>
        <head>
            <style>
                .content {{
                    background: -webkit-linear-gradient(0deg, #39b1b2, #000000 100%);
                    padding: 2rem;
                }}
                .content p {{
                    margin-bottom: 1rem;
                }}
                .scores {{
                    display: flex;
                    flex-direction: row;
                    justify-content: space-between;
                    font-size: 1.1em;
                    margin-top: 1.5rem;
                    margin-bottom: 2rem;
                }}
                .score {{
                    text-align: center;
                }}
                .report {{
                    font-size: 1.2em;
                    line-height: 1.6;
                    margin-bottom: 2rem;
                }}
                .logo img {{
                    height: 150px;
                    width: auto;
                    padding-top: 1rem;
                }}
            </style>
        </head>
        <body>
            <div class="content">
                <p style="font-size: 1.5em;">Dear Participant,</p>
                <p style="font-size: 1.3em;">Congratulations! You have completed your interview through DevHire.</p>
                <div class="scores">
                    <div class="score">
                        <p>Speech</p>
                        <p>{scores[0]}/10.0</p>
                    </div>
                    <div class="score">
                        <p>Understanding</p>
                        <p>{scores[1]}/10.0</p>
                    </div>
                    <div class="score">
                        <p>AI Analysis</p>
                        <p>{scores[2]}/10.0</p>
                    </div>
                </div>
                <p style="font-size: 1.2em;">Detailed Report of Your Interview:</p>
                <div class="report">{report}</div>
            </div>
            <div class="logo">
                <img src="https://lh3.googleusercontent.com/drive-viewer/AFGJ81rxuocJq92t5lIyKSE51q-xBEsMu3ah0tJxlnpw_VHkmzZ3NSo1yqWIrd0EI8W3QvSJIIRZgwWx_dEHjVuRkZ7rQYixxw=s2560" alt="logo.png">
            </div>
        </body>
    </html>
    """


    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP_SSL(smtp_server, port, context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Something went wrong while sending the email: {e}")
    finally:
        server.quit()

            
            
