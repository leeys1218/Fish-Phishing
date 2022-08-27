const http = require('http');
const url = require('url');
const spawn = require('child_process').spawn;

var app = http.createServer(function(request, response){

    let _url = request.url
    let target_url = url.parse(_url, true).query.target;
    console.log(target_url);

    let parsed = '{"target_url": "'+ target_url + '",';

    const result = spawn('python', ['MLP_model.py', target_url]);
    result.stdout.on('data', (result) => {
        parsed += result.toString();
        
        response.writeHead(200,
            {
                "Access-Control-Allow-Origin": "*",
            });
        response.end(parsed);
    })
}).listen(3000);

/*
url의 쿼리스트링으로 받고, 결과를 응답해줌

후에 client와 통신과정에서 오류 발생시 
 writehead부분을 손봐야 할 수 있음
*/