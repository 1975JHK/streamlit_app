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
    layout = "wide",
    initial_sidebar_state = "auto"
)

# 4.sidebar 설계
with st.sidebar:
    option = st.selectbox(label = "**이동하려는 페이지 선택:**",
                          options = ["JH Data Lab 소개",
                                     "예제1:Korean Body Shape",
                                     "예제2:Economic Indicators",
                                     "예제3:RealTime Weather",
                                     "예제4:Process Capability"])
    table_btn = st.button(label = "데이터 테이블")
    graph_btn = st.button(label = "데이터 시각화")

# 5.JH DataLab소개
if option == "JH Data Lab 소개":
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
                         s = str(value), fontdict = {"style":"italic", "size":10})
            elif i > 4:
                plt.text(x = i-4.95, y = value,
                         s = str(value), fontdict = {"style":"italic", "size":10})
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
    df = df.iloc[0:, :]
    col_names = df.columns
    colors = ["orange", "green", "steelblue"]
    
    if table_btn:
        st.write("**한국 가계 경제 지표 (한국은행, 2022~2024년 자료)**")
        st.dataframe(data = df, hide_index = True,
                     width = 600, height = 550,
                     column_config={"year":st.column_config.NumberColumn(format="%d")})
    
    elif graph_btn:
        fig = plt.figure(figsize = (8, 6))
        # fig.set_facecolor("#2F2E2E")
        st.write("**월별 가계 경제 지표 추이 (한국은행, 2022~2024년 자료)**")
        for i, name in enumerate(col_names[1:4]):
            plt.plot(df["Month"], df[name], marker = "o",
                    color = colors[i], label = name, markersize = 5.0,
                    linewidth = 2.0)
        plt.legend(loc = "upper left", fontsize = 10)
        plt.xlabel("Month", fontdict = {"weight":"bold", "size":11, "color":"black"})
        plt.ylabel("Index", fontdict = {"weight":"bold", "size":11, "color":"black"})
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.gca().spines["bottom"].set_visible(False)
        plt.gca().spines["left"].set_visible(False)
        plt.ylim(90.0, 115.0)
        plt.yticks(color = "black", size = 9)
        plt.xticks(np.arange(0, df.shape[0], step = 2), color = "black",
                   rotation = 45, size = 9)
        # plt.gca().set_facecolor("#2F2E2E") #배경색
        plt.grid(True)
        st.pyplot(fig)
    
    else:
        st.write("**한국 가계 경제 지표 (한국은행, 2022~2024년 자료)**")
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
        # fig.set_facecolor("#2F2E2E")
        st.write("**전국 주요 도시 {} 온도/습도 (기상청, RSS 서비스)**".format(now))
        ax = fig.subplots()
        ax = plt.gca()
        ax.bar(x = df["City"],height = df["Temp(℃)"], color = "orange",
               alpha = 1.0)
        ax.set_ylabel("Current Temp.(℃)", color = "black", size = 11)
        ax.set_xlabel("Name of City", color = "black", size = 11)
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
        ax2.set_ylabel("Current Humi(%)", color = "black", size = 11)
        ax.legend(["Current Temp(℃)"], loc = "upper right")
        ax2.legend(["Current Humi(%)"], loc = "upper left")
        # ax.set_facecolor("#2F2E2E") #배경색
        ax.grid(True)
        ax.tick_params(axis = "both", colors = "black", labelsize = 10)
        ax2.tick_params(axis = "both", colors = "black", labelsize = 10)
        st.pyplot(fig)
    elif table_btn:
        st.write("**전국 주요 도시 {} 기상 정보 (기상청, RSS 서비스)**".format(now))
        st.dataframe(data = df, use_container_width = True,
                    hide_index = True)
    else:
        st.write("**전국 주요 도시 {} 기상 정보 (기상청, RSS 서비스)**".format(now))
        st.dataframe(data = df, use_container_width = True,
                    hide_index = True)

# 9. 공정 능력 분석(PCI)
if option == "예제4:Process Capability":
    # 입력 widget column 생성
    col1, col2 = st.columns([2, 12])
    with col1:
        st.write("**공정 능력 구하기**")
        type = st.selectbox(label = "spec.형태",
                            options = ["단측:USL", "단측:LSL", "양측:BOTH"], index = 2)
        usl = st.number_input(label = "USL 입력:",
                              value = 15.0)
        lsl = st.number_input(label = "LSL 입력:",
                              value = 5.0)
        mean = st.number_input(label = "평균 입력:",
                               min_value = -100.0, max_value = 2000.0,
                               value = 10.0)
        stdev = st.number_input(label = "표준편차 입력:",
                                min_value = -100.0, max_value = 2000.0,
                                value = 1.0)
        start = st.button(label = "공정 능력 산출")
    with col2:
        # visualization
        if start:
            y = np.random.normal(mean, stdev, 10000)
            data = norm(loc = 0.0, scale = 1.0)
            x = np.linspace(start = np.min(y), stop = np.max(y), num = 10000)
            y1 = norm.pdf(x, mean, stdev)
        
            if type == "단측:USL":
                pci = (usl - mean)/stdev
                prob = (1-data.cdf(pci))*1000000
            elif type == "단측:LSL":
                pci = (mean - lsl)/stdev
                prob = (1-data.cdf(pci))*1000000
            else:
                pci_usl = (usl - mean)/stdev
                pci_lsl = (mean - lsl)/stdev
                prob_usl = (1-data.cdf(pci_usl))*1000000
                prob_lsl = (1-data.cdf(pci_lsl))*1000000
                prob = prob_usl + prob_lsl
                pci = norm.ppf((1-(prob/1000000)))
            print("공정능력(Z):{:.2f}".format(pci))
            print("불량률:{:.0f}ppm".format(prob))
        
            st.write("평균(Mean)과 표준편차(StDev)로 공정능력 파악하기")
            fig = plt.figure()
            plt.plot(x, y1, marker = "", color = "blue", linewidth = 3) 
            plt.hist(x = y, bins = 50, color = "orange", alpha = 0.7, density = True,
                     edgecolor = "black")                         
            plt.grid(True)                                               
            plt.text(x = mean*1.2, y = 0.39, s = "Process Capability(Z):{:.2f}".format(pci),
                    color = "red", fontdict={"style":"italic", "size":12})
            plt.text(x = mean*1.2, y = 0.37, s = "Expected Defective:{:.0f}ppm".format(prob), 
                    color = "red", fontdict={"style":"italic", "size":12})
            if type == "단측:USL":
                plt.vlines(x = [mean, usl], ymin = 0.0, ymax = 0.45, 
                           colors = ["blue", "red"], linestyles = ["dashed", "solid"],
                           label = ["Mean", "USL"])
                plt.text(x = usl, y = 0.45, s = "USL", 
                         color = "red", fontdict={"style":"italic", "size":12})
                plt.text(x = mean, y = 0.45, s = "Mean", 
                         color = "blue", fontdict={"style":"italic", "size":12})
                plt.xlim((np.min(x)-(abs(np.min(x))*0.2), usl+(abs(usl)*0.3)))
            elif type == "단측:LSL":
                plt.vlines(x = [lsl, mean], ymin = 0.0, ymax = 0.45, 
                           colors = ["red", "blue"], linestyles = ["solid", "dashed"])
                plt.text(x = lsl, y = 0.45, s = "LSL", 
                         color = "red", fontdict={"style":"italic", "size":12})
                plt.text(x = mean, y = 0.45, s = "Mean", 
                         color = "blue", fontdict={"style":"italic", "size":12})
                plt.xlim((lsl-(abs(lsl)*0.3), np.max(x)*1.0))
            else:
                plt.vlines(x = [lsl, mean, usl], ymin = 0.0, ymax = 0.45, 
                           colors = ["red", "blue", "red"], linestyles = ["solid", "dashed", "solid"])
                plt.text(x = usl, y = 0.45, s = "USL", 
                         color = "red", fontdict={"style":"italic", "size":12})
                plt.text(x = lsl, y = 0.45, s = "LSL", 
                         color = "red", fontdict={"style":"italic", "size":12})
                plt.text(x = mean, y = 0.45, s = "Mean", 
                         color = "blue", fontdict={"style":"italic", "size":12})
                plt.xlim((lsl-(abs(lsl)*0.3), usl+(abs(usl)*0.3)))
            plt.xlabel("Values Expected", color = "black", fontdict={"size":11})
            plt.ylabel("Probability", color = "black", fontdict={"size":11})
            plt.yticks(color = "black", size = 9)
            plt.xticks(color = "black", size = 9)
            plt.gca().spines["bottom"].set_visible(False)
            plt.gca().spines["top"].set_visible(False)
            plt.gca().spines["left"].set_visible(False)
            plt.gca().spines["right"].set_visible(False)
            st.pyplot(fig)
        else:
            st.markdown("사이드바에서 :green[Spec.형태, USL, LSL, 평균, 표준편차]를 입력하세요!")
            st.markdown(":green[공정능력 산출 버튼]을 누르세요!")
