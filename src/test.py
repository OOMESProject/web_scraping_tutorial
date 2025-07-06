import requests
from bs4 import BeautifulSoup

# 1. 웹 페이지 요청
url = "https://news.ycombinator.com"
response = requests.get(url)

#print(response)

#2.응답 상태 확인
if response.status_code == 200:
    print("페이지를 성공적으로 가져왔습니다!")
else:
    print("페이지를 가져오는데 실패했습니다. 상태 코드: {response.status_code}")
    exit()
