import time, requests, re
import pandas as pd
import streamlit as st

class Weather:
    def __init__(self):
        # 대한민국 주요 지역 URL
        self.urls = [
        "https://www.kma.go.kr/w/rss/dfs/hr1-forecast.do?zone=1168052100",
        "https://www.kma.go.kr/w/rss/dfs/hr1-forecast.do?zone=3023052000",
        "https://www.kma.go.kr/w/rss/dfs/hr1-forecast.do?zone=2726067000",
        "https://www.kma.go.kr/w/rss/dfs/hr1-forecast.do?zone=2611057000",
        "https://www.kma.go.kr/w/rss/dfs/hr1-forecast.do?zone=2611057000",
        "https://www.kma.go.kr/w/rss/dfs/hr1-forecast.do?zone=5013025300",
        "https://www.kma.go.kr/w/rss/dfs/hr1-forecast.do?zone=3114056000",
        "https://www.kma.go.kr/w/rss/dfs/hr1-forecast.do?zone=2817770000",
        "https://www.kma.go.kr/w/rss/dfs/hr1-forecast.do?zone=4111366200"]

        # 대한민국 주요 지역 명칭
        self.names = ["서울", "대전", "대구", "부산", "광주", "제주", "울산", "인천", "수원"]

        # 기상 상태, 기온 및 습도 저장을 위한 빈 리스트 생성
        self.skies = []
        self.temps = []
        self.humis = []

    # 주요 지역별 기상 정보 읽어 와서 출력 및 저장하기
    def real_time_weather(self):
        empty = st.empty()
        for i, url in enumerate(self.urls):
            # 프로그레스바 진척율 표시
            with empty:
                percent = (i + 1) / len(self.urls)
                st.progress(value = percent, text = "기상정보 크롤링 중...")
                # 기상청 RSS URL(주소)에서 html 가져오기
            response = requests.get(url)
            # 읽어온 html에서 하늘상태/기온/습도만 추출하기
            wfor = re.findall("<wfKor>(.+)</wfKor>", response.text)[1]
            temp = re.findall("<temp>(.+)</temp>", response.text)[1]
            humi = re.findall("<reh>(.+)</reh>", response.text)[1]
            # 날씨 정보 저장하기 
            self.skies.append(wfor)
            self.temps.append(float(temp))
            self.humis.append(float(humi))
        # 날씨 정보 데이터 프레임으로 저장하기
        names = ["Seoul", "Daejeon", "Daegu", "Pusan", "Kwangju", 
                "Jeju", "Ulsan", "Incheon", "Suwon"]
        weather = pd.DataFrame(zip(names, self.skies, self.temps, self.humis), 
                            columns = ["City", "Sky", "Temp(℃)", "Humi(%)"])
        empty.write("크롤링이 완료되었습니다.")
        return weather
