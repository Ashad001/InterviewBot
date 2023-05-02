from flask import Flask, request, jsonify
from flask import render_template
from main import Interview
from reportMailscript import send_mail


interviews = [None] * 100
 
def get_interview_index(user_id):
    for i in range(len(interviews)):
        if interviews[i] is not None and interviews[i].user_id == str(user_id):
            return i
    return None

app =  Flask(__name__,template_folder="templates")

@app.route("/")
def aut():
    return render_template("InterviewBot.html")

interview_index = int(-1)
@app.route("/starter",methods=["POST","GET"])
def runner():
    global interview_index
    data = request.get_json()
    user_id = str(data["user_id"])
    print("user id: ", user_id)
    interview_index = get_interview_index(user_id)
    if interview_index is None:
        for i in range(len(interviews)):
            if interviews[i] is None:
                interview_temp = Interview("Maaz", user_id)
                interviews[i] = interview_temp
                interview_index = int(i)
                break
    result = interviews[int(interview_index)].run(str(data["prompt"]))
    print("index: ", interview_index, result)
    return str(result[0])
@app.route("/receive-data",methods=["POST","GET"])
def receive_data():
    data = request.get_json()
    print(interview_index)
    result = interviews[interview_index].run(str(data))
    scores = result[2] # Scores: [Tone, Understanding, Bot]
    if result[1] == 0:
        scores = scores
        report = interviews[interview_index].get_report_data()
        send_mail("ashad001sp@gmail.com", scores=scores, report=report)
        interviews[interview_index] = None
        exit()
    response = {"ans": result[0], "score": scores}
    return jsonify(response)

if __name__ == "__main__":
    app.run()