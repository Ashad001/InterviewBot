# DevHire 🤖📝

DevHire is an InterviewBot designed to assist students, fresh graduates, and interns in preparing for technical and behavioral interviews. It utilizes sentiment analysis to provide scores in three sections: tone, understanding, and overall assessment. Additionally, it generates a detailed report for each candidate, including their background, strengths, areas for improvement, and recommendations. The bot also incorporates a user authentication system using a signin/signup page to identify users and store their information in a Google Sheets database. Interviews conducted by DevHire typically consist of a maximum of 20 questions.

## Features

✅ Signin/Signup Page: Users can create an account or sign in to access DevHire's interview services.

📊 Sentiment Analysis: DevHire uses sentiment analysis to evaluate and score the candidate's responses in three sections: tone, understanding, and overall assessment.

📋 Detailed Report: After the interview, DevHire generates a comprehensive report for each candidate. The report includes their background information, identified strengths, areas for improvement, and personalized recommendations.

📧 Email Notifications: DevHire automatically sends the generated reports to the candidates via email, ensuring they receive their interview results promptly.

## Installation

To make contribution to DevHire, follow these steps:

1. Fork the repository

2. Clone the repository
```bash
git clone https://github.com/your-username/DevHire.git
```

2. Install the required dependencies:

```bash
cd DevHire
pip install -r requirements.txt
```

3. Set up the Google Sheets integration:

   - Create a Google Sheets document and generate API credentials.
   - Update the `config.js` file with your API credentials and the Google Sheets document ID.

4. Configure email settings:

   - Update the `config.js` file with your email service provider's SMTP settings.
   - Make sure to provide the necessary authentication details for sending emails.

5. Start the application:

```shell
python devhire_googlesheets.py
```

6. Open your web browser and navigate to `http://localhost:3000` to access the DevHire application.

## Usage

1. Sign up for an account or sign in if you already have one.
2. Provide your interview details, such as your name, background, and preferred interview type (technical or behavioral).
3. Begin the interview by clicking the "Start Interview" button.
4. DevHire will present questions to you, one at a time. Take your time to answer each question thoughtfully.
5. After completing all the questions or ending the interview early, DevHire will process your responses and generate a report.
6. You will receive an email with your detailed report, including scores in the tone, understanding, and overall sections, as well as recommendations for improvement.

## Technologies Used

- Python 
- Flask
- JavaScript
- Google Sheets API
- Sentiment Analysis Library (NLTK, TextBlob)

## Contributors

- Ashad Abdullah ([@Ashad001](https://github.com/Ashad001))
- Maaz Imam ([@Maaz-Imam](https://github.com/Maaz-Imam))
- Dinesh Dhanji ([@Dinesh Dhanji](https://github.com/DineshDhanji))
- Aheed Tahir ([@Tahiralira](https://github.com/Tahiralira))
- Abdul Haseeb ([@abdulhaseeb-user](https://github.com/abdulhaseeb-user))
- Laiba Meer ([@LaibaMeer](https://github.com/LaibaMeer))

## License

This project is licensed under the [MIT License](LICENSE).

---

We hope that DevHire will assist you in preparing for your interviews! Good luck! 🚀🎉