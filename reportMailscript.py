import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re



def send_mail(recievermail, scores, report):
    port = 465  # For SSL
    receiver_email = recievermail
    # read mail from file
    with open("/static/readmail.txt") as f:
        sender_email = f.read()
    # password read from file
    with open("/static/password.txt") as f:
        password = f.read()


    smtp_server = "smtp.gmail.com"
    scores = scores
    report = report
    message = MIMEMultipart("alternative")
    message["Subject"] = "Score and Report"
    message["From"] = sender_email
    message["To"] = receiver_email

    formatreport = re.split(r'\r?\n|\r|\n|(\w+):', str(report))

    report = " "
    for line in formatreport:
        if line is not None:
            report = report + line + '<br>'

    text = f"Hi,\n\nHere are your scores\n Score By Tone: {scores[0]} / 10.0\n Score by Question Understanding {scores[1]} / 10.0\n Score By Bot: {scores[2]} \ 10.0.\n\n{report}"
    # HTML content
    html = f"""
    <html>
  <head>
    <title>Report</title>
    <style>
      .contain {{
        width: 80%;
        margin: 0 auto;
        text-align: right;
        text-justify: inter-word; /* optional */
      }}
      .container {{
        width: 80%;
        margin: 0 auto;
        text-align: justify;
        text-justify: inter-word; /* optional */
      }}
      .content{{
        color:white;
      }}
      .scores {{
        font-size: 1.1em;
        margin-top: 1.5rem;
        margin-bottom: 2rem;
        justify-content: space-evenly;
        flex-direction: column;
      }}
      .score {{
        text-align: center;
      }}
      .report {{
        text-align: left;
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
  <body style="color:white;">
    <div class="content">
    <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
      <div style="margin:50px auto;width:80%;padding:20px 0">
        <div style="border-bottom:5px solid #eee">
        <img src="/static/email_logo.png" alt="logo.png"  style="display:float; margin:auto;" height="150" width=auto>
        </div>
        <div style="color:white; text-align:center; background: -webkit-linear-gradient(0deg,#39b1b2 ,#000000 100%);">

          <p style="font-size:15px">
            <b>Dear Participant,</b>
          </p>
          <p>Congratulations! You have completed your interview through DevHire.</p>
          <div class="scores">
            <div class="score">
              <p>Score By Tone</p>
              <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{scores[0]}/10.0</h2>
            </div>
            <div class="score">
              <p>Score by Question Understanding</p>
              <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{scores[1]}/10.0</h2>
            </div>
            <div class="score">
              <p>Score By Bot</p>
              <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{scores[2]}/10.0</h2>
            </div>
          </div>
          <h3 class="container">Detailed Report of Your Interview:</h3>
          <div class="container">{report}</div>
          <p class="contain" style="font-size:15px;">
            Regards,<br />Team DevHire
          </p>
        </div>
        <hr style="border:none;border-top:5px solid #eee" />
        <div style="float:left;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
          <p>Contact Us</p>
          <p>
            <a href="mailto:devhirecontact@gmail.com">info@devday.com</a>.
          </p>
        </div>
      </div>
    </div>
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
        # print("Email sent successfully!")
    except Exception as e:
        # print(f"Something went wrong while sending the email: {e}")
    finally:
        server.quit()
