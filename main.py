import openai
import os
from textblob import TextBlob
import re
from flask import Flask, request, jsonify, render_template
from flask import session
from reportMailscript import send_mail
from flask_cors import CORS
import pandas as pd
import gspread


# from flask import Flask, request, render_template
# from reportMailscript import send_mail

try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except:
    print("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

def safe_division(numerator, denominator):
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return numerator

def report_maker(questions, format_style, answers, model = "gpt-3.5-turbo", max_tokens = 250):
    messages = [
        {"role": "system", "content": f"In a recent interivew with following questions {questions}\n and candidate has responded with following answers to each of the questions {answers}\n\n Make a report of the interview and areas where the candidate can improve that can be sent to candidate for future use!\n No need to write each question and answer, just write the report and areas where the candidate can improve!"},
        {"role": "user", "content": format_style}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=max_tokens,
    )
    return response.choices[0].message['content']

def score_maker(question, answer, model = "gpt-3.5-turbo", max_tokens = 1):
    # parse format_style to comma separated string
    messages = [
        {"role": "system", "content": f"Rate the message given out of 10 (Be more lenient), based on its correctness, tone and overall behaviour comparing with the question asked! Only write the score where you can (no need to explain the score) otherwise score 0'."},
        {"role": "user", "content": f"Question: {question}, Anwer: {answer}, Score: "}
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=max_tokens,
    )
    return response.choices[0].message['content']

class Interview:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.messages = [
            {
            "role": "system",
            "content": "You are a interviewer named DevHire and you are interviewing a candidate for a job. \
                        You are asking the candidate about his/her experience. \
                        You can ask about the candidate's previous work experience, education, or anything else you think is relevant to the job. \
                        Assess the candidate's ability to analyze problems and provide effective solutions. Can they think critically and creatively to solve complex problems?  \
                        You can also ask the candidate about various programming questions such as code completion and bug fixes. \
                        Assess whether the candidate's values, personality, and work style align with the company culture and team dynamics \
                        User will answer your questions one by one and you have to verify whether it is correct or not, its overall behaviour and tone throughout the interview should also be noted. "
            },
        ]

        self.score_message = [
            {
                "role": "assistant",
                "content": "Rate the message given out of 10, based on its correctness, tone and overall behaviour comparing with the question asked! Only write the score where you can (no need to explain the score) otherwise score 0'.",
            }
        ]

        self.score_pattern = re.compile(r'\d+')
        self.scoreByAnswer = 0
        self.scoreByTone = 0
        self.scoreByBot = 0
        self.x_value = 0
        self.questionsAsked = 0

        self.currentTone = 0.0;
        self.currentUnderstanding = 0.0;
        self.currentBot = 0.0


        self.scoreCount_0 = 0
        self.scoreCount_1 = 0
        self.scoreCount_2 = 0
        self.stop_patterns = [
            r".*(stop|end|pause|break|reschedule|leave|close|not interested|not ready).*interview.*",
        ]
        self.questions = []
        self.answers = []

        self.patterns = [
            r'(if|do) you have any (questions|concerns)',
            r'Let me know if you change your mind\b',
            r'(?:Is there anything else you would like to add|Do you have any questions for us?)\??',
            r'Good luck with your job search(?!.*Good luck with your job search)',
            r"we'll keep you updated on any developments",
            r'thank you for your time',
            r"thank\s+you(\s+very\s+much)?\s+for\s+your\s+time",
            r"(?i)\b(thank\s*you(?:\s*very\s*much)?|(?:thanks|thankyou)(?:\s+(?:very\s+much))?)(?:\s*(?:for)\s*your\s*time)\b",
        ]
    def process_message(self, message):
        if self.questionsAsked == 0 and not (message.startswith(("My name is", r"Hi(,?) I am", r"Hi(,?) My name is", r"Hello(,?) My name is", r"Hello(,?) I am"))):
           message = "My name is {} ".format(self.name) + message

        # Bot Prompt
        self.messages.append({"role": "user", "content": message})
        try:
            self.chatbot = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
        except Exception as e:
            return -2

        reply = self.chatbot.choices[0].message.content
        self.messages.append({"role": "system", "content": reply})

        # Stop_words checkings for the bot
        if any(re.match(pattern, message, re.IGNORECASE) for pattern in self.stop_patterns):
            return 0

        if self.questionsAsked > 19:
            return 1
        # Stop_words checkings for the bot
        for pattern in self.patterns:
            match = re.search(pattern, reply, flags=re.IGNORECASE)
            if match or self.questionsAsked > 4:
                return 1

        self.questions.append(reply)
        if self.questionsAsked > 0:
            self.answers.append(message)

        # Score Calculations
        blobReply = TextBlob(reply)
        blobMessage = TextBlob(message)
        tone_score = blobMessage.sentiment.polarity
        understanding_score = blobReply.sentiment.polarity

        self.currentTone = 0.65 * self.currentTone
        self.currentUnderstanding = 0.65 * self.currentUnderstanding
        self.currentBot = 0.65 * self.currentBot

        if self.questionsAsked >= 1:
            score1 = ((tone_score + 1) * 5)
            score2 = ((understanding_score + 1) * 5)

            score0 = score_maker(self.questions[-2], self.answers[-1], model="gpt-3.5-turbo", max_tokens=1)
            # print(score0)
            if score0.isdigit() and score0 is not None and score0 != "0" and score0 != "0.0":
                self.scoreCount_0 += 1
                self.currentBot = float(score0)
                self.scoreByBot += self.currentBot
            if score1 > 0.5:
                self.scoreCount_1 += 1
                self.currentTone = score1
            if score2 > 0.5:
                self.scoreCount_2 += 1
                self.currentUnderstanding = score2
            self.scoreByTone += score1
            self.scoreByAnswer += score2
        self.questionsAsked += 1
        # Tone Checkings
        if self.questionsAsked > 5 and self.scoreByTone < 2:
            return -1

        return reply

    def get_report_data(self):
        format_style = 'Report:: Candidate Background: , Strengths: ,Areas To Improve: ,Recomendations: ,'
        report = report_maker(self.questions, format_style, self.answers, model="gpt-3.5-turbo", max_tokens=250)
        return report

    def run(self,message):
        if message:
            try:
                scores = []
                response = self.process_message(message)
                scores.append(round(safe_division(self.scoreByTone, self.scoreCount_1), 1))
                scores.append(round(safe_division(self.scoreByAnswer, self.scoreCount_2), 1))
                scores.append(round(safe_division(self.scoreByBot, self.scoreCount_0), 1))
                if response == 0:
                    BotAnswer = "Interview stopped. Thank you for your time."
                    BotStatus = 0
                elif response == 1:
                    BotAnswer = "Interview completed. It was great interviewing you\n"
                    BotStatus = 0
                elif response == -1:
                    response = "Interview stopped. \nUnfortunately, we can't continue with the interview at this time due to the tone of our interaction. Thank you for your time."
                elif response == -2:
                    return "Something went wrong. Please try again."
                else:
                    BotAnswer = response
                    BotStatus = 1
                if BotStatus == 0:
                    scores.append(round(safe_division(self.scoreByTone, self.scoreCount_1), 1))
                    scores.append(round(safe_division(self.scoreByAnswer, self.scoreCount_2), 1))
                    scores.append(round(safe_division(self.scoreByBot, self.scoreCount_0), 1))
                elif BotStatus == 1:
                    scores.append(round(self.currentTone, 1))
                    scores.append(round(self.currentUnderstanding, 1))
                    scores.append(round(self.currentBot, 1))
                return BotAnswer,BotStatus, scores
            except Exception as e:
                print(e)
                print("Something went wrong. Please try again.")


interviews = [None] * 100

def get_interview_index(user_id):
    for i in range(len(interviews)):
        if interviews[i] is not None and interviews[i].user_id == str(user_id):
            return i
    return None

app =  Flask(__name__,template_folder="templates")
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = os.urandom(24)


@app.route("/")
def aut():
    return render_template("InterviewBot.html")

@app.route("/starter",methods=["POST","GET"])
def runner():
    global kkkk
    user_id = str(request.json["user_id"])
    print("user id: ", user_id)
    interview_index = session.get('interview_index', None)
    kkkk = interview_index
    if interview_index is None:
        for i in range(len(interviews)):
            if interviews[i] is None:
                interview_temp = Interview("Maaz", user_id)
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
    data = request.json
    interview_index = session.get('interview_index', None)
    result = interviews[int(interview_index)].run(str(data))
    scores = result[2]
    flag = 1
    report = interviews[int(interview_index)].get_report_data()
    send_mail("ashad001sp@gmail.com", scores=scores, report=report)
    response = jsonify({"ans":"The Interview has ended, please check your email for the detailed report of this session.\nThank you for speaking with us. To have another session please login again.","score":scores, "flag":flag})
    interviews[int(interview_index)] = None
    session.pop('interview_index', None)
    return response

if __name__ == "__main__":
    app.run()