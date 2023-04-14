import openai
import os
from textblob import TextBlob
import re

openai.api_key = os.environ["OPENAI_API_KEY"]

messages = [
    {
        "role": "system",
        "content": "You are a interviewer and you are interviewing a candidate for a job. \
                    You are asking the candidate about his/her experience. \
                    You can ask about the candidate's previous work experience, education, or anything else you think is relevant to the job. \
                    You can also ask the candidate about various programming questions such as code completion and bug fixes. \
                    User will answer the question and you have to verify whether it is correct or not!. \
                    And also rate the answer's accuracy between 0 and 10 (10 being most suitable answer) and display in ['accuracy'] at the very end of each response. To stop the interview, please type 'stop'.",
    },
]



stop_words = ["stop", "quit", "exit", "end", "finish"]

while True:
    message = input("user: ")
    if message:
        if any(word in message.lower() for word in stop_words):
            print("Interview stopped.")
            print("Please complete the interview before requesting a score.")
            break
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat.choices[0].message.content
        print(f"Chatbot: {reply}")
        messages.append({"role": "system", "content": reply})
        blob = TextBlob(reply)
        tone_score = blob.sentiment.polarity
        accuracy = round((tone_score + 1) * 5)
        print(f"Accuracy: {accuracy}")
        