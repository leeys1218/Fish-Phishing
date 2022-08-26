chrome.tabs.query({ currentWindow: true, active: true }, function(tabs){
	fetch('http://localhost:3000/?target='+tabs[0].url)
        .then((response)=>{
        return response.text();
    }).then((response)=>{
        console.log(1)
        var info = document.createElement("button")
        var infoText = document.createTextNode("자세히 알아보기...")
        info.appendChild(infoText)
        info.onclick = function(){
            location.href = 'info.html'
        }
        document.body.appendChild(info);
        console.log(2)
        if (response == 1) {
            document.getElementsByTagName("h1")[0].innerHTML = "이 사이트는 안전해요!"
            return document.getElementById("image").src="image/isnotPhishing.png"
        }
        else if (response == 0){
            document.getElementsByTagName("h1")[0].innerHTML = "이 사이트는 위험합니다!"
            return document.getElementById("image").src="image/isPhishing.png"
        }
    })
})

