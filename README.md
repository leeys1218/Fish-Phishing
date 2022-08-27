# 2021 Hanium Project
# 머신러닝을 활용한 Phishing Site(피싱 사이트) 사전 탐지 프로그램
#### Project title : Fish-Phishing
#### Project period : 2021.05 ~ 2021.11
-----------------------
## Description


## Run
크롬 확장프로그램에서 파이썬 코드를 실행시키기 까다로워 머신러닝 예측을 요청받고 응답받는 외부 서버를 제작하였지만,
현재 배포하고 있지 않아 본 프로젝트의 서버 파일을 로컬 환경에서 실행하여 프로그램을 사용할 수 있습니다.

client/app 파일을 자신의 크롬 확장프로그램으로 로드하고, server/server.js 파일을 노드로 실행
### 크롬 확장프로그램으로 로드하기
```
https://support.google.com/chrome/a/answer/2714278?hl=ko#
```
### node 서버 실행하기
```
node server.js
```
### Environment
Node 16.17.0 (window)

Python 3.7.9 (window)

### Prerequisite
Python Library
> pip install pandas
>
> pip install ssl
>
> pip install whois
>
> pip install torch
>
> pip install tld
