<script>
        window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new window.SpeechRecognition();
        recognition.interimResults = false;
        let listening = false;
        let stoppeer = document.getElementById('stoppage');
        let text = document.getElementById('InputField');
        let send_arrow = document.getElementById('textArrow');
        let text_area = document.getElementById('textArea');
        let info = document.getElementById('infoicon');
        let rules = document.getElementById('rulesarea');
        let start = document.getElementById('start');
        let input = document.getElementById('input');
        let score = document.getElementById('score');
        let voice_arrow = document.getElementById('voiceArrow');
        // let stBD = document.getElementById('staticBackdrop');

        text_area.style.display = 'none';
        input.className += ' blur';
        score.className += ' blur';
        // stBD.className += 'blur';
        text.disabled = true;

        stoppeer.style.cursor = 'default';
        stoppeer.style.opacity = 0.5;
        stoppeer.onclick = 'null';
        send_arrow.style.opacity = 0.5;
        send_arrow.onclick = 'null';
        send_arrow.style.cursor = 'default';
        voice_arrow.classList.remove('fa-beat');
        voice_arrow.style.opacity = 0.5;
        voice_arrow.onclick = 'null';
        voice_arrow.style.cursor = 'default';

        // var sessionTimeout = 30000;
        // var sessionTimeoutId;
        // function resetSessionTimeout() {
        //   clearTimeout(sessionTimeoutId);
        //   sessionTimeoutId = setTimeout(endSession, sessionTimeout);
        // }

        // document.addEventListener('mousemove', resetSessionTimeout);
        // document.addEventListener('keypress', resetSessionTimeout);
        // window.addEventListener('beforeunload', endSession);

        // function endSession() {
        //   fetch('/end-session')
        //     .then(response => response.text())
        //     .then(data => {
        //         disableInput();
        //         createEl('bot', data);
        //         text_area.scrollTop = text_area.scrollHeight;
        //     })
        //     .catch(error => console.error(error));
        // }



        function voice() {
            if (!listening) {
                console.log("DevHire is listening.");
                voice_arrow.classList.add('fa-beat');
                recognition.start();
                listening = true;
            }
            else {
                console.log("DevHire is already listening.");
            }
        }

        recognition.addEventListener("result", (e) => {
            const voice_input = Array.from(e.results)
                .map((result) => result[0])
                .map((result) => result.transcript)
                .join("");
            if (e.results[0].isFinal) {
                if (text.value != "") {
                    text.value += " ";
                    text.value += voice_input;
                }
                else {
                    text.value += voice_input;
                }
                active(text);
            }
            else {
                if (text.value != "") {
                    text.value += " ";
                    text.value += voice_input;
                }
                else {
                    text.value += voice_input;
                }
                active(text);
            }
            voice_arrow.classList.remove('fa-beat');
        });

        recognition.addEventListener("end", () => {
            console.log("DevHire stopped listening.");
            listening = false;
            voice_arrow.classList.remove('fa-beat');
        });

        function check(event) {
            if (event.key == "Enter" && !event.shiftKey) {
                event.preventDefault();
                send();
                // text.disabled = false;
                // voice_arrow.style.opacity = 1;
                // voice_arrow.style.cursor = 'pointer';
                // voice_arrow.addEventListener("click", voice);
            }
        }

        function active(msg) {
            if (msg.value.trim() != "") {
                send_arrow.style.opacity = 1;
                send_arrow.style.cursor = 'pointer';
                send_arrow.addEventListener("click", send);
            }
            else {
                send_arrow.style.opacity = 0.5;
                send_arrow.onclick = 'null';
                send_arrow.style.cursor = 'default';
            }
        }

        function send() {
            console.log("Message Sent.");
            text.disabled = true;
            send_arrow.onclick = 'null';
            send_arrow.style.cursor = 'default';
            voice_arrow.style.opacity = 0.5;
            voice_arrow.removeEventListener("click", voice);
            voice_arrow.style.cursor = 'default';
            listening = false;
            voice_arrow.classList.remove('fa-beat');
            if (text.value.length > 0) {
                createEl('user', "");
                active(text);
                text_area.scrollTop = text_area.scrollHeight;

                fetch("/receive-data", {
                    method: "POST",
                    body: JSON.stringify(text.value),
                    headers: {
                        "Content-Type": "application/json"
                    },
                })
                    .then(response => response.json())
                    .then(data => {
                        var Botdata = data.ans;
                        var scoresList = data.score;
                        var flag = data.flag;
                        if(parseInt(flag)==1)
                        {
                            disableInput();
                        }
                        createEl('bot', Botdata);
                        adjust_Scores(scoresList);
                        text_area.scrollTop = text_area.scrollHeight;
                    })
                    .catch(error => console.error(error));
            }
            text.value = "";
        }

        function createEl(inp, data) {
            if (inp === 'user') {
                var div1 = document.createElement('div');
                div1.classList.add('IntervieweeDiv', 'offset-2', 'col-10');

                var div2 = document.createElement('div');
                div2.className += 'IntervieweeIcon';

                var i1 = document.createElement('i');
                i1.classList.add('bi', 'bi-person');
                div2.appendChild(i1);

                var div3 = document.createElement('div');
                div3.classList.add('IntervieweeChat', 'col-11');

                var s1 = document.createElement('p');
                s1.classList.add('fs-6');
                s1.innerText = text.value;
                div3.appendChild(s1);

                div1.appendChild(div3);
                div1.appendChild(div2);
                text_area.appendChild(div1);
                // iterateWithDelay(text.value,s1,20);
            }
            else if (inp === 'bot') {
                var div1 = document.createElement('div');
                div1.classList.add('InterviewBotDiv', 'col-10');

                var div2 = document.createElement('div');
                div2.className += 'InterviewBotIcon';

                var i1 = document.createElement('i');
                i1.classList.add('bi', 'bi-robot');
                div2.appendChild(i1);

                var div3 = document.createElement('div');
                div3.classList.add('InterviewBotChat', 'col-11');

                var p1 = document.createElement('p');
                p1.className += 'fs-6';
                p1.innerText = data;
                div3.appendChild(p1);

                div1.appendChild(div2);
                div1.appendChild(div3);
                text_area.appendChild(div1);
                console.log(data);
                // iterateWithDelay(data,p1,20);
            }
        }

        function iterateWithDelay(array, ele, delay) {
            let index = 0;
            function loop() {
                ele.innerText += array[index];
                index++;
                if (index < array.length) {
                    setTimeout(loop, delay);
                }
            }
            setTimeout(loop, delay);
        }
        function generateUserId()
        {
            const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
            let result = '';
            for(let i=0;i<16;i++)
            {
                result += chars[Math.floor(Math.random() * chars.length)];
            }
            console.log(result)
            return result;
        }

        function startInt() {
            text.disabled = false;
            text_area.style.display = 'block';
            score.classList.remove('blur');
            input.classList.remove('blur');
            // stBD.classList.remove('blur');
            rules.style.display = 'none';
            start.onclick = 'null';
            voice_arrow.style.opacity = 1;
            voice_arrow.style.cursor = 'pointer';
            voice_arrow.addEventListener("onclick", voice);

            const userID = generateUserId();
            const prompt = "Please start the interview";


            fetch("/starter", {
                method: "POST",
                body: JSON.stringify({"user_id": userID, "prompt": prompt}),
                headers: {
                    "Content-Type": "application/json"
                },
            })
                .then(response => response.json())
                .then(data => {
                    createEl('bot', data.result);
                    text_area.scrollTop = text_area.scrollHeight;
                })
                .catch(error => console.error(error));
        }

        function adjust_Scores(scoresList) {
            var tone_score = scoresList[0];
            var und_score = scoresList[1];
            var AI_score = scoresList[2];

            document.getElementById('tone').innerHTML = tone_score;
            document.getElementById('understanding').innerHTML = und_score;
            document.getElementById('AIscore').innerHTML = AI_score;
            document.getElementById('tone2').innerHTML = tone_score;
            document.getElementById('understanding2').innerHTML = und_score;
            document.getElementById('AIscore2').innerHTML = AI_score;

            tone_score = tone_score * 10;
            und_score = und_score * 10;
            AI_score = AI_score * 10;

            document.getElementById('tone-bar').style.width = tone_score + '%';
            document.getElementById('und-bar').style.width = und_score + '%';
            document.getElementById('ai-bar').style.width = AI_score + '%';
            document.getElementById('tone-bar2').style.width = tone_score + '%';
            document.getElementById('und-bar2').style.width = und_score + '%';
            document.getElementById('ai-bar2').style.width = AI_score + '%';
        }

        function disableInput()
        {
            input.style.display = 'none';
            text.disabled = true;
            send_arrow.removeEventListener("click", send);
            send_arrow.style.cursor = 'default';
            voice_arrow.style.opacity = 0.5;
            voice_arrow.removeEventListener("click", voice);
            voice_arrow.style.cursor = 'default';
            listening = false;
            voice_arrow.classList.remove('fa-beat');
            stoppeer.removeEventListener("click", stopper);
            stoppeer.style.cursor = 'default';
            stoppeer.style.opacity = 0.5;
        }

        function stopper()
        {
            console.log("STOP INTERVIEW CALLED");
            // fetch("/stopper_yay", {
            //     method: "POST",
            //     body: JSON.stringify("Stop the Interview"),
            //     headers: {
            //         "Content-Type": "application/json"
            //     },
            // })
            //     .then(response => response.json())
            //     .then(data => {
            //         createEl('bot', data.result);
            //         text_area.scrollTop = text_area.scrollHeight;
            //     })
            //     .catch(error => console.error(error));
        }
    </script>