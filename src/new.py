import pandas as pd
import requests
from datetime import datetime, timedelta
from dateutil import parser
import time
import urllib.parse
from bs4 import BeautifulSoup

# KRX 데이터 가져오기
def get_krx_data(date_str):
    # KRX 정보데이터시스템 URL (POST 요청)
    url = "http://data.krx.co.kr/comm/bldAttendant/executeForResourceBundle.cmd"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # 요청 파라미터 (코스피/코스닥 전체 종목)
    payload = {
        "bld": "dbms/MDC/STAT/standard/MDCSTAT01501",
        "mktId": "ALL",  # 코스피+코스닥
        "trdDd": date_str.replace("-", ""),  # 예: 20250707
        "share": "1",
        "money": "1",
        "csvxls_isNo": "false"
    }
    
    # 데이터 요청
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code != 200:
        print(f"KRX 데이터 요청 실패: {response.status_code}")
        return None
    
    # JSON 데이터 파싱
    data = response.json()
    if "OutBlock_1" not in data:
        print("KRX 데이터 파싱 실패: 데이터 없음")
        return None
    
    df = pd.DataFrame(data["OutBlock_1"])
    return df

# 상위 10% 상승 종목 선정
def get_top_risers(df):
    if df is None or df.empty:
        return None
    
    # 등락률을 숫자로 변환 (FLUC_RT: 등락률)
    df["FLUC_RT"] = pd.to_numeric(df["FLUC_RT"], errors="coerce")
    # 등락률 기준 내림차순 정렬
    df_sorted = df.sort_values(by="FLUC_RT", ascending=False)
    # 상위 10% 계산
    top_n = int(len(df_sorted) * 0.1)
    top_risers = df_sorted.head(top_n)[["ISU_SRT_CD", "ISU_ABBRV", "FLUC_RT"]]
    return top_risers

# 네이버 뉴스 검색 (웹 스크래핑 방식)
def search_naver_news(stock_name, date_str):
    query = f"{stock_name} 주가 상승"
    encoded_query = urllib.parse.quote(query)
    url = f"https://search.naver.com/search.naver?where=news&query={encoded_query}&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds={date_str}&de={date_str}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return f"네이버 뉴스 검색 실패: {stock_name}"
    
    soup = BeautifulSoup(response.text, "html.parser")
    news_items = soup.select("a.news_tit")
    
    results = []
    for item in news_items[:3]:  # 상위 3개 기사만
        title = item.get_text().strip()
        link = item.get("href")
        results.append({"title": title, "link": link})
    
    return results if results else f"{stock_name} 관련 뉴스 없음"

# 메인 함수
def main():
    # 오늘 날짜 (예: 2025-07-07)
    today = datetime.now().strftime("%Y%m%d")
    date_str = datetime.now().strftime("%Y.%m.%d")
    
    # KRX 데이터 가져오기
    print(f"{date_str} 주식 데이터 가져오는 중...")
    df = get_krx_data(today)
    if df is None:
        print("데이터를 가져올 수 없습니다.")
        return
    
    # 상위 10% 상승 종목
    top_risers = get_top_risers(df)
    if top_risers is None:
        print("상위 상승 종목을 선정할 수 없습니다.")
        return
    
    print(f"\n{date_str} 상위 10% 상승 종목:")
    print(top_risers[["ISU_ABBRV", "FLUC_RT"]])
    
    # 각 종목에 대해 네이버 뉴스 검색
    for _, row in top_risers.iterrows():
        stock_name = row["ISU_ABBRV"]
        print(f"\n{stock_name} 관련 뉴스 검색 중...")
        news_results = search_naver_news(stock_name, date_str)
        
        if isinstance(news_results, str):
            print(news_results)
        else:
            print(f"{stock_name} 관련 뉴스:")
            for news in news_results:
                print(f"- {news['title']} ({news['link']})")
        
        time.sleep(1)  # 서버 부하 방지

# 실행
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        main()