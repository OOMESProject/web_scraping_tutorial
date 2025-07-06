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

#3.HTML 파싱
'''
soup = BeautifulSoup(response.text, 'html.parser')
#html문서내용 출력됨
print(soup)
'''

#테스트용 HTML
html =""""
<nav class="menu-box-1" id="menu-box">
 <ul>
  <li>
   <a class="naver" href="https://www.naver.com">네이버로 이동</a>
  </li>
  <li>
   <a class="google" href="https://www.google.com">구글로  이동</a>
  </li>
  <li>
   <a class="daum" href="https://www.daum.com">다음으로 이동</a>
  </li>
 </ul>
</nav>
"""

soup = BeautifulSoup(html, 'html.parser')