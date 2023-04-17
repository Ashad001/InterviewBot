import openai
import os
from textblob import TextBlob
import re

openai.api_key = os.environ["OPENAI_API_KEY"]


class Interview:
    def __init__(self, name):
        self.messages = [
            {
                "role": "system",
                "content": "You are a interviewer and you are interviewing a candidate for a job. \
                            You are asking the candidate about his/her experience."
            },
        ]
        self.name = name
        self.score_pattern = re.compile(r'\d+')
        self.scoreByAnswer = 0
        self.scoreByTone = 0
        self.x_value = 0
        self.questionsAsked = 0
        
        self.stop_patterns = [
            r".*(stop|end|pause|break|reschedule|leave|not interested|not ready).*interview.*",
        ]
        
        self.patterns = [
            r'\d+/10',
            r'\d+\s*(?:\/|out of)\s*\d+',
      

        ]
        # self.chatbot = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
    def process_message(self, message):
        if self.questionsAsked == 0 and not (message.startswith(("My name is", r"Hi(,?) I am", r"Hi(,?) My name is"))):
           message = "My name is {} ".format(self.name) + message

        words = message.lower().split()
        self.messages.append({"role": "user", "content": message})
        self.chatbot = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
        reply = self.chatbot.choices[0].message.content
        blob = TextBlob(message)
        
        if any(re.match(pattern, message, re.IGNORECASE) for pattern in self.stop_patterns):
            print(message);
            print("Interview stopped.")
            print("Please complete theInterview before requesting a score.")
            return 0
        for pattern in self.patterns:
            match = re.search(pattern, reply, flags=re.IGNORECASE)
            if match:
                self.x_value = match.group(1)
                print("Interview completed.")
                # print(f"Score: {self.x_value}")
                return self.x_value
    
        self.messages.append({"role": "system", "content": reply})
        tone_score = blob.sentiment.polarity
        accuracy = round((tone_score + 1) * 5)
        print(accuracy)
        self.scoreByTone += accuracy
        self.questionsAsked += 1
        return reply, accuracy

    def run(self):
        while True:
            message = input("user: ")
            if message:
                response = self.process_message(message)
                if response == 0:
                    break
                if response == self.x_value:
                    self.scoreByTone / self.questionsAsked
                    print(f"Your Score By Correctness is: {response}")
                    print(f"Your Score By Tone is: {self.scoreByTone / self.questionsAsked}")
                    break
                if response:
                    print(f"Chatbot: {response[0]}")
                    # print(f"Accuracy: {response[1]}")


if __name__ == "__main__":
    # Name of candidate will be fetched from the google sheets
    interview = Interview("Ali")
    interview.run()
    
            # if any(re.match(pattern, reply, re.IGNORECASE) for pattern in self.patterns):
        #     self.x_value = re.findall(self.score_pattern, reply)[0]
        #     print("Interview completed.")
        #     return self.x_value

      # r'score\s*:\s*(\d+)/\d+',
            # r'final\s*rating\s*:\s*(\d+)/\d+',
            # r'\d+\s+stars',
            # r'rated\s*(\d+)\s*out of \d+',
            # r'(\d+)/\d+\s*points',
            # r'got\s*(\d+)\s*out of 10',
            # r'rate your interview\s+(\d+)\s+out of \d+',
            # r'give you a score of\s+(\d+)\s+out of \d+',
            # r'your performance\s*(\d+)\s*\/\s*\d+',
            # r'I would give you (\d+) stars of \d+',
            # r'you scored\s*(\d+)\s*out of a possible \d+\s*(?:.*\n)*?(thank you for your time|we\'ll keep you updated on any developments)',
            # r'thank you for your (time|answer|response)',
            # r'if you have any (questions|concerns)',
            # r'Let me know if you change your mind\b',
            # r"we'll keep you updated on any developments",
            # r'(?:Is there anything else you would like to add|Do you have any questions for us?)\??',
            # r'It was nice to talk to you',
            # r'Good luck with your job search(?!.*Good luck with your job search).*'

                        # You can ask about the candidate's previous work experience, education, or anything else you think is relevant to the job. \
                            # Assess the candidate's ability to analyze problems and provide effective solutions. Can they think critically and creatively to solve complex problems?  \
                            # You can also ask the candidate about various programming questions such as code completion and bug fixes. \
                            # Assess whether the candidate's values, personality, and work style align with the company culture and team dynamics \
                            # User will answer the question and you have to verify whether it is correct or not, its overall behaviour and tone throughout the interview. \
                            # And also rate the answer's accuracy between 0 and 10 (10 being most suitable answer) at the very end of each response. If you are done with the interview , type the score and type 'Thank you for visiting' " ,

# messages = [
#     {
#         "role": "system",
#         "content": "You are a interviewer and you are interviewing a candidate for a job. \
#                     You are asking the candidate about his/her experience. \
#                     You can ask about the candidate's previous work experience, education, or anything else you think is relevant to the job. \
#                     Assess the candidate's ability to analyze problems and provide effective solutions. Can they think critically and creatively to solve complex problems?  \
#                     You can also ask the candidate about various programming questions such as code completion and bug fixes. \
#                     Assess whether the candidate's values, personality, and work style align with the company culture and team dynamics \
#                     User will answer the question and you have to verify whether it is correct or not, its overall behaviour and tone throughout the interview. \
#                     And also rate the answer's accuracy between 0 and 10 (10 being most suitable answer) at the very end of each response. If you are done with the interview , type the score and type 'Thank you for visiting' " ,
#     },
# ]


# stop_patterns = [
#     r".*(stop|end|pause|break|reschedule|leave|not interested).*interview.*",
#     r".*(stop|end|pause|break|reschedule|leave|not interested).*",
# ]

# patterns = [
#     r"Thank you for your time today\.?\s?Based on your responses,? I would rate you \d+ out of 10\.?",
#     r"Your answers were (well[- ]thought out|insightful) and informative\.? I would give you a score of \d+ out of 10\.?",
#     r"It was a pleasure speaking with you today\.?\s?In my opinion,? you deserve a score of \d+ out of 10\.?",
#     r"Your problem-solving skills are impressive\.? I would rate you \d+ out of 10\.?",
#     r"Thank you for your (insights|perspectives)\.?\s?Based on your responses,? I would give you a score of \d+ out of 10\.?",
#     r"Your communication skills are (top-notch|impressive)\.? I would rate you \d+ out of 10\.?",
#     r"It'?s? clear that you have a deep understanding of the (industry|subject)\.? I would give you a score of \d+ out of 10\.?",
#     r"Your ability to think critically and creatively was (evident|impressive) throughout the interview\.?\s?In my opinion,? you deserve a score of \d+ out of 10\.?",
#     r"I appreciate your (enthusiasm|passion) for the job\.?\s?Based on your responses,? I would rate you \d+ out of 10\.?",
#     r"Your (experience|expertise) is (impressive|notable)\.?\s?I would give you a score of \d+ out of 10\.?",
#     r"It'?s? (evident|clear) that you have a (strong|great) work ethic and dedication to your craft\.?\s?In my opinion,? you deserve a score of \d+ out of 10\.?",
#     r"Your responses were (insightful|well-articulated)\.?\s?Based on your performance today,? I would rate you \d+ out of 10\.?",
#     r"Thank you for your (patience|professionalism) throughout the interview\.? I would give you a score of \d+ out of 10\.?",
#     r"Your (attention to detail|ability to analyze complex issues) were (impressive|notable)\.?\s?In my opinion,? you deserve a score of \d+ out of 10\.?",
#     r"Your (positive attitude|teamwork skills) were (notable|impressive)\.?\s?Based on your responses,? I would rate you \d+ out of 10\.?",
#     r"Thank you for your time today\.?\s?(Based on your responses,)? I would rate you \d+ out of 10\.?",
#     r"Your answers were (well[- ]thought out|insightful) and informative\.? ?I would give you a score of \d+ out of 10\.?",
#     r"It was a pleasure speaking with you today\.?\s?(In my opinion,)? you deserve a score of \d+ out of 10\.?",
#     r"Your problem-solving skills are (impressive|notable)\.? ?I would rate you \d+ out of 10\.?",
#     r"Thank you for your (insights|perspectives)\.?\s?(Based on your responses,)? I would give you a score of \d+ out of 10\.?",
#     r"Your communication skills are (top[- ]notch|impressive)\.? ?I would rate you \d+ out of 10\.?",
#     r"(It'?s?|This is) clear that you have a (deep|great) understanding of the (industry|subject)\.? ?I would give you a score of \d+ out of 10\.?",
#     r"Your ability to (think critically|creatively) was (evident|impressive) throughout the interview\.?\s?(In my opinion,)? you deserve a score of \d+ out of 10\.?",
#     r"I appreciate your (enthusiasm|passion) for the job\.?\s?(Based on your responses,)? I would rate you \d+ out of 10\.?",
#     r"Your (experience|expertise) is (impressive|notable)\.?\s?(I would give you a score of|You scored) \d+ out of 10\.?",
#     r"(It'?s?|This is) (evident|clear) that you have a (strong|great) work ethic and dedication to your craft\.?\s?(In my opinion,)? you deserve a score of \d+ out of 10\.?",
#     r"Based on your performance today,? your responses were (insightful|well-articulated)\.?\s?I would rate you \d+ out of 10\.?",
#     r"Thank you for your (patience|professionalism) throughout the interview\.? ?I would give you a score of \d+ out of 10\.?",
#     r"Your (attention to detail|ability to analyze complex issues) were (notable|impressive)\.?\s?(In my opinion,)? you deserve a score of \d+ out of 10\.?",
#     r"Based on your responses,? your (positive attitude|teamwork skills) were (notable|impressive)\.?\s?I would rate you \d+ out of 10\.?",
#     r"I would rate you \d+ out of 10\. Your responses today were (well[- ]thought out|insightful)\.",
#     r"I would give you a score of \d+ out of 10\. Your answers were (well[- ]thought out|informative)\.",
#     r"I would rate you \d+ out of 10\. In my opinion, you showed a (deep|impressive) understanding of the (industry|subject)\.",
#     r"I would give you a score of \d+ out of 10\. Your ability to analyze complex issues and think creatively was (impressive|notable)\.",
#     r"Based on your performance today, I would rate you \d+ out of 10\. Your responses were (insightful|well-articulated)\.",
#     r"I would give you a score of \d+ out of 10\. Your experience and expertise are (impressive|notable)\.",
#     r"I would rate you \d+ out of 10\. It's evident that you have a (strong|great) work ethic and dedication to your craft\.",
#     r"Based on your responses, I would give you a score of \d+ out of 10\. Your problem-solving skills are (impressive|notable)\.",
#     r"I would rate you \d+ out of 10\. Your communication skills are (top-notch|impressive)\.",
#     r"I would give you a score of \d+ out of 10\. Your positive attitude and teamwork skills were (notable|impressive)\.",
#     r"Based on your responses, I would rate you \d+ out of 10\. Your attention to detail was (impressive|notable)\."
# ]


# The blob.sentiment.polarity function returns a value between -1 and 1.
# The value represents the sentiment polarity of a given text 
# Where -1 is very negative, 0 is neutral, and 1 is very positive.
# I have converted this into a range of 1 to 10, where 1 is very negative and 10 is very positive.
