const signinSendOtp = document.getElementById("signinSendOtp");
const signinTimer = document.getElementById("signinTimer");
const signinButton = document.getElementById("signinButton");
const email = document.getElementById('signinEmail');
const signinOtp = document.getElementById('signinOtp');
signinButton.style.display = 'none';
signinOtp.style.display = 'none';

function sendOtp(button, timer, emailInput) {
button.disabled = true;
let timeRemaining = 120;
timer.innerHTML = `OTP sent! Expires in ${timeRemaining} seconds.`;

const countdown = setInterval(() => {
    timeRemaining--;
    timer.innerHTML = `OTP sent! Expires in ${timeRemaining} seconds.`;

    if (timeRemaining <= 0) {
    clearInterval(countdown);
    button.disabled = false;
    timer.innerHTML = "OTP expired. Click Send OTP to request a new one.";
 }
}, 1000);
}

function validateEmail() {
const pattern = /^\w+([.-]?\w+)@\w+([.-]?\w+)(\.\w{2,3})+$/;
return pattern.test(email.value);
}

function verifyemail() {
if(validateEmail()){
sendOTP();
setTimeout(function(){
signinButton.style.display = 'block';
signinOtp.style.display = 'block';
}, 1500);
}
else{
alert("Incorrect Email Format Entered , Use a Valid Email Please")
}
}

var OTPcode;
function sendOTP() {
  sendOtp(signinSendOtp, signinTimer, email);
  var obj = {"email": email.value };
  fetch("/sendOTP", {
    method: "POST",
    body: JSON.stringify(obj),
    headers: {
      "Content-Type": "application/json"
    },
  })
    .then(response => response.text())
    .then(data => {
      OTPcode = parseInt(data);

      if (OTPcode === 742) {
        window.location.href = "/signinerror";
      }
    })
    .catch(error => console.error(error));
}

function checkOTP() {
if(OTPcode == parseInt(signinOtp.value)) {
getValues();
} else {
console.log("Incorrect OTP");
alert("Incorrect OTP. Please try again.");
}
}

var toneScore;
var understandingScore;
var aiAnalysisScore;
var first_name;

function showWelcomeSection() {
// Hide the sign-in section and show the welcome section
document.getElementById("signin").style.display = "none";
const welcomeh1a = document.querySelector("#welcomeh1");
welcomeh1a.textContent = "Welcome Back " + first_name;
document.getElementById("welcome").style.display = "block";
document.getElementById("toneScore").innerHTML = `Tone Score: ${toneScore}`;
document.getElementById("understandingScore").innerHTML = `Understanding Score: ${understandingScore}`;
document.getElementById("aiAnalysisScore").innerHTML = `AI Analysis Score: ${aiAnalysisScore}`;
}

function getValues(){
    fetch("/get_values", {
              method: "POST",
              body: JSON.stringify({"email": email.value}),
              headers: {
                  "Content-Type": "application/json"
              },
          })
              .then(response => response.json())
              .then(data => {
                first_name = data.fname;
                toneScore = data.tone;
                understandingScore = data.und;
                aiAnalysisScore = data.ai;
                console.log(first_name,toneScore,understandingScore,aiAnalysisScore);
                localStorage.setItem('first', first_name);
                localStorage.setItem('em', email.value);
                showWelcomeSection();
              })
              .catch(error => console.error(error));

            }

function interviewStart()
{
window.location.href = "/interview";
}