# 1.필요한 라이브러리 호출
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
from PIL import Image
import time, requests, re

# 2.시각화 기본 설정
font_path = "NanumGothic.ttf"
font = font_manager.FontProperties(fname = font_path).get_name()
rc('font', family=font)
matplotlib.rcParams["font.size"] = 7
matplotlib.rcParams["axes.unicode_minus"] = False

# 3.페이지 기본 설정
st.set_page_config(
    page_title = "JH DataLab",
    page_icon = ":bulb:",
    layout = "centered",
    initial_sidebar_state = "auto"
)

# 4.sidebar 설계
with st.sidebar:
    option = st.selectbox(label = "**Choose One To Know:**",
                          options = ["Introduction",
                                     "Economic Indicators",
                                     "RealTime Weather"])
    table_btn = st.button(label = "데이터 테이블")
    graph_btn = st.button(label = "데이터 시각화")
    

# 5.JH DataLab소개
if option == "Introduction":
    history = [
    "JH DataLab은...",
    ":seedling: 데이터 분석 전문 회사입니다.",
    ":palm_tree: 복잡 다단한 현상의 이해와 일상의 의사결정에 불확실을 줄여드립니다.",
    ":evergreen_tree: 분석 내용은 시각화 도구를 이용하여 당신이 쉽게 이해하도록 돕겠습니다.",
    ":deciduous_tree: 수학, 통계, 머신러닝 및 Big Data 분석에 이르는 다양한 분야의 도구를 사용합니다."]
    st.subheader("**We will help you to make your works :green[simple] and :green[easy].**", divider = "gray")
    con = st.container(border = True)
    for word in history:
        con.write(word)
        con.write("\n")
        time.sleep(1.5)
    image = Image.open("good_logo.jpg")
    con.image(image, use_column_width = True)


# 6.주요 경제 지표
if option == "Economic Indicators":
    file_paths = [
    "경제심리지수.csv",
    "소비자물가지수.csv",
    "주택매매가격지수.csv"]
    names = ["Economic Sentiment Index", "Consumer Price Index", 
             "House Price Index"]
    for i, file in enumerate(file_paths):
        df_i = pd.read_csv(r"{}".format(file), index_col = 0).transpose()
        df_i = df_i.iloc[3:, :]
        df_i = df_i.reset_index()
        df_i.columns = ["Month", names[i]]
        if i == 0:
            df = df_i.copy()
        elif i == 1:
            df_i = df_i.iloc[1:, :]
        if i >= 1:
            df = df.merge(df_i, how = "outer", on = "Month")
    df = df.iloc[0:-1, :]
    col_names = df.columns
    colors = ["orange", "green", "steelblue"]
    
    if table_btn:
        st.write("**한국 가계 경제 지표**")
        st.dataframe(data = df, hide_index = True,
                     width = 600, height = 550,
                     column_config={"year":st.column_config.NumberColumn(format="%d")})
    
    elif graph_btn:
        fig = plt.figure(figsize = (8, 6))
        fig.set_facecolor("#2F2E2E")
        st.write("**월별 가계 경제 지표 추이**")
        for i, name in enumerate(col_names[1:4]):
            plt.plot(df["Month"], df[name], marker = "o",
                    color = colors[i], label = name, markersize = 3.5,
                    linewidth = 1.5)
        plt.legend(loc = "upper left", fontsize = 10)
        plt.xlabel("Month", fontdict = {"weight":"bold", "size":11, "color":"white"})
        plt.ylabel("Index", fontdict = {"weight":"bold", "size":11, "color":"white"})
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.gca().spines["bottom"].set_visible(False)
        plt.gca().spines["left"].set_visible(False)
        plt.ylim(85.0, 115.0)
        plt.yticks(color = "white", size = 9)
        plt.xticks(np.arange(0, df.shape[0], step = 2), color = "white",
                   rotation = 45, size = 9)
        plt.gca().set_facecolor("#2F2E2E") #배경색
        plt.grid(True)
        st.pyplot(fig)
    
    else:
        st.write("**한국 가계 경제 지표**")
        st.dataframe(data = df, hide_index = True,
                     width = 600, height = 550,
                     column_config={"year":st.column_config.NumberColumn(format="%d")})


# 7. 실시간 날씨 정보
# 7-1.실시간 기상정보 크롤링
def real_time_weather():
    # 대한민국 주요 지역 URL
    urls = [
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
    names = ["서울", "대전", "대구", "부산", "광주", "제주", "울산", "인천", "수원"]

    # 기상 상태, 기온 및 습도 저장을 위한 빈 리스트 생성
    skies = []
    temps = []
    humis = []

    # 주요 지역별 기상 정보 읽어 와서 출력 및 저장하기
    for i, url in enumerate(urls):
        # 기상청 RSS URL(주소)에서 html 가져오기
        response = requests.get(url)
        # 읽어온 html에서 하늘상태/기온/습도만 추출하기
        wfor = re.findall("<wfKor>(.+)</wfKor>", response.text)[0]
        temp = re.findall("<temp>(.+)</temp>", response.text)[0]
        humi = re.findall("<reh>(.+)</reh>", response.text)[0]
        # 날씨 정보 저장하기 
        skies.append(wfor)
        temps.append(float(temp))
        humis.append(float(humi))
    # 날씨 정보 데이터 프레임으로 저장하기
    weather = pd.DataFrame(zip(names, skies, temps, humis), 
                        columns = ["지역", "기상", "기온(℃)", "습도(%)"])
    return weather

# 7-1. 날씨정보 테이블
if option == "RealTime Weather":
    df = real_time_weather()
    now = dt.datetime.now().strftime("%y/%m/%d %H:%M")
if graph_btn:
        fig = plt.figure(figsize = (8, 6))
        fig.set_facecolor("#2F2E2E")
        st.write("**전국 주요 도시 {} 온도/습도 정보**".format(now))
        ax = fig.subplots()
        ax = plt.gca()
        ax.bar(x = df["City"],height = df["Temp(℃)"], color = "orange",
               alpha = 1.0)
        ax.set_ylabel("Current Temp.(℃)", color = "white", size = 11)
        ax.set_xlabel("Name of City", color = "white", size = 11)
        ax2 = ax.twinx()
        ax2 = plt.gca()
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.spines["left"].set_visible(False)
        ax2.spines["top"].set_visible(False)
        ax2.plot(df["City"], df["Humi(%)"], marker = "o", linewidth = 2.0,
                 color = "green")
        ax2.set_ylabel("Current Humi(%)", color = "white", size = 11)
        ax.legend(["Current Temp(℃)"], loc = "upper right")
        ax2.legend(["Current Humi(%)"], loc = "upper left")
        ax.set_facecolor("#2F2E2E") #배경색
        ax.grid(True)
        ax.tick_params(axis = "both", colors = "white", labelsize = 10)
        ax2.tick_params(axis = "both", colors = "white", labelsize = 10)
        st.pyplot(fig)
    elif table_btn or option == "RealTime Weather":
        st.write("**전국 주요 도시 {} 기상 정보**".format(now))
        st.dataframe(data = df, use_container_width = True,
                    hide_index = True)
        
