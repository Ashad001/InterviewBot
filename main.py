import openai
import os
from textblob import TextBlob
import re

try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except:
    print("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    

class Interview:
    def __init__(self, name):
        self.messages = [
            {
            "role": "system",
            "content": "You are a interviewer named DevHire and you are interviewing a candidate for a job. \
                        You are asking the candidate about his/her experience. \
                        You can ask about the candidate's previous work experience, education, or anything else you think is relevant to the job. \
                        Assess the candidate's ability to analyze problems and provide effective solutions. Can they think critically and creatively to solve complex problems?  \
                        You can also ask the candidate about various programming questions such as code completion and bug fixes. \
                        Assess whether the candidate's values, personality, and work style align with the company culture and team dynamics \
                        User will answer the your series of questions and you have to verify whether it is correct or not, its overall behaviour and tone throughout the interview. "
            },
        ]
        self.score_message = [ 
            {
                "role": "assistant",
                "content": "Rate the message given out of 10, based on its correctness, tone and overall behaviour comparing with the question asked! Only write the score where you can (no need to explain the score) otherwise score 0'.",   
            }
        ]
        self.name = name
        self.score_pattern = re.compile(r'\d+')
        self.scoreByAnswer = 0
        self.scoreByTone = 0
        self.scoreByBot = 0
        self.x_value = 0
        self.questionsAsked = 0
        self.stop_patterns = [
            r".*(stop|end|pause|break|reschedule|leave|close|not interested|not ready).*interview.*",
        ]
        
        self.patterns = [
            r'(if|do) you have any (questions|concerns)',
            r'Let me know if you change your mind\b',
            r'(?:Is there anything else you would like to add|Do you have any questions for us?)\??',
            r'Good luck with your job search(?!.*Good luck with your job search)', 
            r'thank you for your time',
            r"we'll keep you updated on any developments",
            r"thank\s+you(\s+very\s+much)?\s+for\s+your\s+time",
            r"(?i)\b(thank\s*you(?:\s*very\s*much)?|(?:thanks|thankyou)(?:\s+(?:very\s+much))?)(?:\s*(?:for)\s*your\s*time)\b",
        ]
    def process_message(self, message):
        if self.questionsAsked == 0 and not (message.startswith(("My name is", r"Hi(,?) I am", r"Hi(,?) My name is", r"Hello(,?) My name is", r"Hello(,?) I am"))):
           message = "My name is {} ".format(self.name) + message

        # Bot Prompt
        self.messages.append({"role": "user", "content": message})
        try:
            self.chatbot = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages, max_tokens = 450)
        except Exception as e:
            return -2
            
        
        reply = self.chatbot.choices[0].message.content
        self.messages.append({"role": "system", "content": reply})

        # Score Prompt
        self.score_message.append({"role": "user", "content": message})
        try:
            self.scoreBot = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.score_message, max_tokens = 1)
        except Exception as e:
            return -2
        score0 = self.scoreBot.choices[0].message.content
        
        # Stop_words checkings for the bot
        if any(re.match(pattern, message, re.IGNORECASE) for pattern in self.stop_patterns):
            return 0
        
        # Stop_words checkings for the bot
        for pattern in self.patterns:
            match = re.search(pattern, reply, flags=re.IGNORECASE)
            if match or self.questionsAsked > 19:
                return 1

        # Score Calculations
        blobReply = TextBlob(reply)
        blobMessage = TextBlob(message)
        tone_score = blobMessage.sentiment.polarity
        understanding_score = blobReply.sentiment.polarity
        score1 = round((tone_score + 1) * 5)
        score2 = round((understanding_score + 1) * 5)
        if score0.isdigit():
            self.scoreByBot += int(score0)
        else:
            self.scoreByBot += 0
        self.scoreByTone += score1
        self.scoreByAnswer += score2
        self.questionsAsked += 1
        
        # Tone Checkings
        if self.questionsAsked > 5 and self.scoreByTone < 3:
            return -1
        return reply

    def run(self):
        message = input("user: ")
        if message:
            try:
                response = self.process_message(message)
                if response == 0:
                    BotAnswer = "Interview stopped.\n Your Score By Tone is: {:.2f} \nYour Score By Understanding is: {:.2f} \nYour Score By Bot is: {}".format(
                        self.scoreByTone / self.questionsAsked, self.scoreByAnswer / self.questionsAsked, self.scoreByBot)
                    BotStatus = 0
                elif response == 1:
                    BotAnswer = "Interview completed. Great, It was great interviewing you\n Your Score By Tone is: {:.2f} \nYour Score By Understanding is: {:.2f} \nYour Score By Bot is: {}".format(
                        self.scoreByTone / self.questionsAsked, self.scoreByAnswer / self.questionsAsked, self.scoreByBot)
                    BotStatus = 0
                elif response == -1:
                    response = "Interview stopped. \nUnfortunately, we can't continue with the interview at this time due to the tone of our interaction. Thank you for your time."     
                elif response == -2:
                    return "Something went wrong. Please try again."
                else:
                    BotAnswer = response
                    BotStatus = 1
                return BotAnswer, BotStatus
            except Exception as e:
                print(e)
                print("Something went wrong. Please try again.")
                    
                    


if __name__ == "__main__":
    # Name of candidate will be fetched from the google sheets
    interview = Interview("Ashad")
    while True:
        returnAns = interview.run()
        print("Bot: ", returnAns[0])
        if returnAns[1] == False:
            break
    