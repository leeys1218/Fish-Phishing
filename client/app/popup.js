
chrome.tabs.query({ currentWindow: true, active: true }, function(tabs){
	fetch('http://localhost:3000/?target='+tabs[0].url)
        .then((response)=>{
        return response.text();
    }).then((response)=>{
        const resJson = JSON.parse(response);
        var info = document.createElement("button")
        var infoText = document.createTextNode("자세히 알아보기...")
        info.appendChild(infoText)
        info.onclick = function(){
            var list = document.querySelector("#list")
            list.innerHTML += "<정상: 1, 의심: 0, 비정상: -1><br>"
            list.innerHTML += "url 주소 길이: " + resJson.Check_URLLength + "<br>"
            list.innerHTML += "url 심볼 포함 여부: " + resJson.Check_Symbol + "<br>"
            list.innerHTML += "도메인 등록 기간: " + resJson.Check_RegiLength + "<br>"
            list.innerHTML += "서브 도메인 유무: " + resJson.Check_SubDomain + "<br>"
            list.innerHTML += "믿을만한 SSL 기관: " + resJson.Check_SSLnOrg + "<br>"
            list.innerHTML += "정상적인 HTTPS: " + resJson.Check_IsHttps
        }
        document.body.appendChild(info);
        console.log(resJson);
        if (resJson.isbenign == '1') {
            document.getElementsByTagName("h1")[0].innerHTML = "이 사이트는 안전해요!";
            return document.getElementById("image").src="image/isnotPhishing.png"       
        }
        else if (resJson.isbenign == '-1' || resJson.isbenign == '0'){
            document.getElementsByTagName("h1")[0].innerHTML = "이 사이트는 위험합니다!";
            return document.getElementById("image").src="image/isPhishing.png"
        }
    })
})

