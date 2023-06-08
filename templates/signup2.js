const signupSendOtp = document.getElementById("signupSendOtp");
const signupTimer = document.getElementById("signupTimer");
const signupButton = document.getElementById("signupButton");
const signupOtp = document.getElementById("signupOtp");
const firstName = document.getElementById('signupFirstName');
const lastName = document.getElementById('signupLastName');
const email = document.getElementById('signupEmail');

signupButton.style.display = 'none';
signupOtp.style.display = 'none';

function sendOtp() {
  signupSendOtp.disabled = true;
  let timeRemaining = 120;
  signupTimer.innerHTML = `OTP sent! Expires in ${timeRemaining} seconds.`;

  // Implement your OTP sending functionality here, using the email from emailInput.value

  const countdown = setInterval(() => {
    timeRemaining--;
    signupTimer.innerHTML = `OTP sent! Expires in ${timeRemaining} seconds.`;

    if (timeRemaining <= 0) {
      clearInterval(countdown);
      signupSendOtp.disabled = false;
      signupTimer.innerHTML = "OTP expired. Click Send OTP to request a new one.";
   }
  }, 1000);
}


function Fvalidate_name() {
let pattern = /^[a-zA-Z]+$/;
return pattern.test(firstName.value);
}

function Lvalidate_name() {
let pattern = /^[a-zA-Z]+$/;
return pattern.test(lastName.value);
}

function validateEmail() {
const pattern = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/;
return pattern.test(email.value);
}


function checkNIG()
{
  if(Fvalidate_name())
  {
     if(Lvalidate_name()){
        if(validateEmail())
        {
            sendOTP();
            setTimeout(function(){
            signupButton.style.display = 'block';
            signupOtp.style.display = 'block';
            }, 1500);

        }
        else{
          alert("Incorrect Email Format Entered , Use a Valid Email Please")
        }
    }
    else{
      alert("Incorrect Last Name Format Entered , Use a Valid Name Please")

    }
  }
  else{
    alert("Incorrect First Name Format Entered , Use a Valid Name Please")
  }
}

var OTPcode;
function sendOTP() {
  sendOtp();
  var obj = { "first": firstName.value, "last": lastName.value, "email": email.value };
  fetch("/getOTP", {
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
        window.location.href = "/signuperror";
      }
    })
    .catch(error => console.error(error));
}

var first;
var last;
var emailVal;

function checkOTP()
{
  signupButton.disabled = true;
  if(OTPcode===parseInt(signupOtp.value))
  {
    var obj = {"first":firstName.value,"last":lastName.value,"email":email.value};
    fetch("/enterinsheet", {
              method: "POST",
              body: JSON.stringify(obj),
              headers: {
                  "Content-Type": "application/json"
              },
          })
              .then(response => response.json())
              .then(data => {
                first = data.first;
                emailVal = data.email;
                localStorage.setItem('first', first);
                localStorage.setItem('em', emailVal);
                console.log("RE");

                window.location.href = "/interview";
              })
              .catch(error => console.error(error));
  }
  else
  {
    console.log("NOT NOT");
  }
}