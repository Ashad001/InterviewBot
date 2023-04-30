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

scores = [10, 10, 10]
report = "Report: The candidate has an undergraduate degree from FAST and has worked on some projects with student organizations, including chatbots. During the interview, the candidate discussed a chatbot project they worked on with a team to answer frequently asked questions for an event. They used Python and specific libraries such as nltk, sklearn, and numpy. Strengths: - The candidate has experience working on chatbot projects and has knowledge of Python libraries used in chatbot development. Areas to Improve: - The candidate lacks professional work experience, which may be a disadvantage when applying for jobs. - During the interview, the candidate did not provide specific examples of their contributions to the chatbot project or how they overcame challenges during development. Providing more detailed information about their experiences and problem-solving skills could make them a stronger candidate. Recommendations: - The candidate should consider gaining more professional work experience through internships or entry-level positions to strengthen their resume. - In future interviews, the candidate should be prepared to provide specific examples of their contributions to projects and how they overcame challenges. This will demonstrate their problem-solving skills and make them a more competitive candidate."
send_mail("ashad001sp@gmail.com", scores, report)