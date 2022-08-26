var objShell = new ActiveXObject("WScript.Shell")
var runProgram = "cmd.exe /k notepad.exe"

chrome.tabs.query({ currentWindow: true, active: true }, function(tabs){
    let target_url = tabs[0].url;
    console.log(0);
    const result = spawn('python', ['MLP_model.py', target_url])// 2. spawn을 통해 "python 파이썬파일.py" 명령어 실행
	result.stdout.on('data', (result) => {
        console.log(1)
        var info = document.createElement("button")
        var infoText = document.createTextNode("자세히 알아보기...")
        info.appendChild(infoText)
        info.onclick = function(){
        location.href = 'info.html'
        }
        document.body.appendChild(info);
        console.log(2)
        if (result == 1) {
            document.getElementsByTagName("h1")[0].innerHTML = "이 사이트는 안전해요!"
            return document.getElementById("image").src="image/isnotPhishing.png"
        }
        else if (result == 0){
            document.getElementsByTagName("h1")[0].innerHTML = "이 사이트는 위험합니다!"
            return document.getElementById("image").src="image/isPhishing.png"
        }
    })
})

