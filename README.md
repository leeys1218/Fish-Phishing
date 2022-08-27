# 2021 Hanium Project
# 머신러닝을 활용한 Phishing Site(피싱 사이트) 사전 탐지 프로그램
#### Project title : Fish-Phishing
#### Project period : 2021.05 ~ 2021.11
-----------------------
## Description


### 실행 화면
> 추가된 확장 프로그램 및 실행 후 로딩
>
> ![image](https://user-images.githubusercontent.com/95534831/187037447-0947bfc0-3226-4968-8b8c-302b5af6761e.png)
> ![loading](https://user-images.githubusercontent.com/95534831/187036900-5d147eb3-adec-4947-a73f-29cfb50fa402.gif)

> 내 github 탭에서 실행 결과
> 
> ![image](https://user-images.githubusercontent.com/95534831/187036936-7e6225ed-da7e-4d16-977c-1f475086072a.png)
> ![image](https://user-images.githubusercontent.com/95534831/187036765-0ebdea56-eaa3-43b4-b1be-27664f7a1145.png)



> 실제 피싱 사이트 탭에서 실행 결과
>
> ![image](https://user-images.githubusercontent.com/95534831/187037206-925558bb-8ffd-4ebc-b0ca-13e46df6317e.png)
> ![image](https://user-images.githubusercontent.com/95534831/187037549-fa024e24-52e2-4db5-ae9a-87c09e83625b.png)
> ![image](https://user-images.githubusercontent.com/95534831/187037277-fccda3e3-5a99-41ad-895c-ebfb70eebf87.png)

(백신 프로그램인 안랩과 동일한 결과)


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
