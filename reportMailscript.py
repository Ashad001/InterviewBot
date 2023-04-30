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
    for lines in formatreport:
        report += (lines + '<br>') 
    
    text = f"Hi,\n\nHere are your scores\n Score By Tone: {scores[0]} / 10.0\n Score by Question Understanding {scores[1]} / 10.0\n Score By Bot: {scores[2]} \ 10.0.\n\n{report}"
    # HTML content
    html = f"""
        <html>
            <body>
                <p>Hi,<br>
                Here are your scores <br> Score By Tone: {scores[0]}/10.0 <br> Score by Question Understanding: {scores[1]}/10.0 <br> Score By Bot: {scores[2]}/10.0.<br>
                <br>
                Detailed Report of Your Interivew <br> <br> { report }<br>
                <br>
                </p>
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
