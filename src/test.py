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
soup = BeautifulSoup(response.text, 'html.parser')  # 네이버의 html 문서가 다 나옴
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
<nav id="hello">어서와</nav>
"""

soup = BeautifulSoup(html, 'html.parser')


print("== find 사용법 ==")
#html 상에 있는 nav를 검색
#그 중에 첫번째 nav를 검색
print(soup.find('nav'))

#html 상에 첫 번째 a 엘리먼트를 검색
print(soup.find('a'))

#html 상에 a를 검색하는데, class 이름이 google인 대상을 검색한다.
print(soup.find('a', class_="google"))

#html 상에 nav를 검색하는데 id가 hello인 대상을 검색한다.
print(soup.find('nav', id="hello"))

print("== find_all ==")

print(soup.find_all('a'))

a_el = soup.find_all('a')

for idx, a in enumerate(a_el):
  #  print(f"{idx} : {a}") 
  #  print(f"{idx} : {a.get_text()}")  # a.get_text() : 엘리먼트를 제외한 텍스트만 추출
  #  print(f"{idx} : {a.get('href')}")
    print(f"{idx} : {a.get('class')}")

# ! select_one : html 상에 첫 번째로 일치하는 요소를 가져옴
print("== select_one 사용법 ==")

print("== 태그로 검색 ==") 
print(soup.select_one('nav'))

print("== 클래스로 검색 ==")
print(soup.select_one('.menu-box-1')) # class가 menu-box-1인 엘리먼트 선택

print("== id로 검색 ==")
print(soup.select_one('#menu-box')) #id 가 menu-box인 엘리먼트 선택

# class 가 daum인 녀석을 검색
#print(soup.select_one('.daum'))

#nav의 자식인 ul, ul의 자식인 li들을 검색 ,검색 결과가 리스트 객체로 변환되어서 나움
print(soup.select_one('nav > ul > li '))

print("== select 사용법 ==")
#nav의 후손인 a 엘리먼트들을 검색
print(soup.select('nav a'))

#반복문
a_el = soup.select('nav a')
for idx, a in enumerate(a_el):
 #print(f"{idx} : {a}")
 #print(f"{idx} : {a.get_text()}")  # 반복문을 이용하여 a엘리먼트의 텍스트만 추출
 #print(f"{idx} : {a.get('href')}")  # 
 print(f"{idx} : {a.get('class')}")  # 



# 대괄호는 '[]'는 속성 선택자
# a[href] : 엘리먼트 a 이면서 속성이 href인 대상을 선택
print(soup.select('a[href]'))