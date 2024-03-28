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
from scipy.stats import norm
from Weather import Weather

# 2.시각화 기본 설정
matplotlib.rcParams["font.family"] = "Malgun Gothic"
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
    option = st.selectbox(label = "**이동하려는 페이지 선택:**",
                          options = ["Data Science 소개",
                                     "예제1:Korean Body Shape",
                                     "예제2:Economic Indicators",
                                     "예제3:RealTime Weather"])
    table_btn = st.button(label = "데이터 테이블")
    graph_btn = st.button(label = "데이터 시각화")
    st.write("---")
    st.write("신체정보입력")
    your_gender = st.selectbox(label = "성별 선택:", options = ["male", "female"],
                               index = 0)
    your_age = st.number_input("연령(나이) 입력", 
                               min_value = 1, max_value = 120, value = 20, step = 1)
    your_height = st.number_input(label = "신장(키) 입력:",
                                  min_value = 10, max_value = 250, value = 170, step = 1)
    prob_btn = st.button(label = "신장(키) 확률")
    

# 5.JH DataLab소개
if option == "Data Science 소개":
    history = [
    "JH DataLab은...",
    ":seedling: 데이터 분석 전문 서비스(Service)를 제공합니다.",
    ":palm_tree: 복잡 다단한 현상의 이해와 일상의 의사결정에 불확실을 줄여드립니다.",
    ":evergreen_tree: 분석 내용은 시각화 도구를 이용하여 당신이 쉽게 이해하도록 돕겠습니다.",
    ":deciduous_tree: 수학, 통계, 머신러닝 및 Big Data 분석에 이르는 다양한 분야의 도구를 사용합니다."]
    st.subheader("**We will help you to make your works :green[simple] and :green[easy].**")
    con = st.container(border = True)
    for word in history:
        con.write(word)
        con.write("\n")
        time.sleep(1.5)
    image = Image.open("good_logo.jpg")
    con.image(image, use_column_width = True)

# 6.한국인 체형
if option == "예제1:Korean Body Shape":
    df_body = pd.read_csv("height.csv")

    if graph_btn:
        st.write("**한국인 성별 연령별 체형 정보 (통계청, 2022년 자료)**")
        fig = plt.figure(figsize = (8, 6))
        # fig.set_facecolor("#2F2E2E")
        sns.barplot(data = df_body, x = "age", y = "mean",
                    hue = "gender", alpha = 0.8)
        for i, value in enumerate(df_body["mean"]):
            if i <= 4:
                plt.text(x = i-0.35, y = value,
                         s = str(value), fontdict = {"weight":"bold", "size":11})
            elif i > 4:
                plt.text(x = i-4.95, y = value,
                         s = str(value), fontdict = {"weight":"bold", "size":11})
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["left"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.gca().spines["bottom"].set_visible(False)
        plt.xlabel("Age", fontdict = {"weight":"bold", "size":11, "color":"black"})
        plt.ylabel("Height(cm)",fontdict = {"weight":"bold", "size":11, "color":"black"})
        plt.legend(loc = "upper right", prop = {"size":12})
        plt.grid(True)
        plt.ylim(150, 182)
        plt.tick_params(axis = "both", labelsize = 10, colors = "black")
        # plt.gca().set_facecolor("#2F2E2E")
        st.pyplot(fig)
        
    elif prob_btn:
        if your_age < 30:
            selected = df_body[(df_body["age"] == 20)&(df_body["gender"] == your_gender)]
            mean = selected.iloc[0, 2]
            std = selected.iloc[0, 3]
        elif 30 <= your_age < 40 :
            selected = df_body[(df_body["age"] == 30)&(df_body["gender"] == your_gender)]
            mean = selected.iloc[0, 2]
            std = selected.iloc[0, 3]
        elif 40 <= your_age < 50 :
            selected = df_body[(df_body["age"] == 30)&(df_body["gender"] == your_gender)]
            mean = selected.iloc[0, 2]
            std = selected.iloc[0, 3]
        elif 50 <= your_age < 60 :
            selected = df_body[(df_body["age"] == 30)&(df_body["gender"] == your_gender)]
            mean = selected.iloc[0, 2]
            std = selected.iloc[0, 3]
            
        y = np.random.normal(mean, std, 10000)   # mean, stdev값을 받아서 10000개의 정규분포 난수 생성
        x = np.linspace(start = np.min(y), stop = np.max(y), num = 1000) # y값의 최대/최소값 범위에서 1000개 등간격 숫자 생성
        y1 = (1 / np.sqrt(2 * np.pi * std**2)) * np.exp(-(x-mean)**2 / (2 * std**2)) # 정규분포 곡선 생성
        prob = round((1-norm.cdf(x = your_height, loc = mean, scale = std))*100, 1) # 정규분포에서 score값 이상의 누적확률 계산 
         
        st.write("당신의 키는 상위 몇%일까?")
        fig = plt.figure(figsize = (8, 6))   # 그래프 객체 fig 생성 : streamlit에서는 명시적으로 생성해야 함
        fig.set_facecolor("#2F2E2E")
        plt.plot(x, y1, marker = "", color = "blue", linewidth = 3) # 정규분포 곡선 작성
        plt.vlines(x = your_height, ymin = 0.0, ymax = 0.1, colors = "red") # score값을 나타내는 수직선 생성
        plt.hist(x = y, bins = 20, color = "orange", alpha = 0.7, density = True)                         # 정규분포값으로 Histogram 생성
        plt.grid(True)                                                # 그래프에 grid 생성
        plt.text(x = your_height, y = 0.065, s = "My Height:{}cm".format(your_height), # score값을 그래프에 출력
                color = "white", fontdict={"style":"italic", "size":12})
        plt.text(x = your_height, y = 0.060, s = "My height from the top:{}%".format(prob), # score값의 상위 누적 확률 출력
                color = "white", fontdict={"style":"italic", "size":12})
        plt.gca().set_facecolor("#2F2E2E")
        plt.xlim((mean-20, mean+20))
        plt.xlabel("Height(cm)", color = "white", fontdict={"size":11})
        plt.ylabel("Probability", color = "white", fontdict={"size":11})
        plt.yticks(color = "white", size = 9)
        plt.xticks(color = "white", size = 9)
        plt.gca().spines["bottom"].set_visible(False)
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["left"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        st.pyplot(fig)     
        
    else:
        st.write("**한국인 체형 정보 (통계청, 2022년 자료)**")
        st.dataframe(data = df_body, hide_index = True,
                     use_container_width = True)


# 7.주요 경제 지표
if option == "예제2:Economic Indicators":
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


# 8. 실시간 날씨 정보
if option == "예제3:RealTime Weather":
    # 8-1.실시간 기상정보 크롤링
    update_weather = st.button("기상정보 Update")
    if update_weather:
        wt = Weather()
        df = wt.real_time_weather()
        df.to_csv("real_time_weather.csv")
    now = dt.datetime.now().strftime("%y/%m/%d %H:%M")
    df = pd.read_csv("real_time_weather.csv")
    df = df.iloc[0:, 1:]
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
    elif table_btn:
        st.write("**전국 주요 도시 {} 기상 정보**".format(now))
        st.dataframe(data = df, use_container_width = True,
                    hide_index = True)
    else:
        st.write("**전국 주요 도시 {} 기상 정보**".format(now))
        st.dataframe(data = df, use_container_width = True,
                    hide_index = True)
