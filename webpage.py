# Updated on 2 July, 2025
# Written by Robin Kim
# 1.필요한 라이브러리 호출
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib, os
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
from PIL import Image
import time, requests, re
from scipy.stats import norm
import requests
from bs4 import BeautifulSoup
from zoneinfo import ZoneInfo
import datetime
from Weather import Weather
from kiwipiepy import Kiwi
from wordcloud import WordCloud
from collections import Counter
import seaborn as sns

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

# 3-1.방문자 수 counting
count = 0
dates = []
visitors = []
def counting_visitors():
    global count
    count += 1
    now = dt.datetime.now().strftime("%y/%m/%d %H:%M:%S")
    with open("visitors_information.csv", mode = "a") as file:
        information = now + "\t" + str(count) +"\n"
        file.write(information)
    with open("visitors_information.csv", mode = "r") as file:
        lines = file.readlines()
        num_visitors = len(lines)
    return num_visitors

    
# 4.sidebar 설계
with st.sidebar:
    option = st.selectbox(label = "**이동하려는 페이지 선택:**",
                          options = ["JH Data Lab 소개",
                                     "예제1:Korean Body Shape",
                                     "예제2:Economic Indicators",
                                     "예제3:RealTime Weather",
                                     "예제4:Process Capability",
                                     "예제5:Newspaper Crawling",
                                     "예제6:Beautiful Korea"])
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
    counting_visitors()
    for word in history:
        con.write(word)
        con.write("\n")
        time.sleep(1.5)
    image = Image.open("good_logo.jpg")
    con.image(image, use_container_width = True)
    
    with open("visitors_information.csv", mode = "r") as file:
        lines = file.readlines()
        visitors = len(lines)
        now = lines[visitors - 1][0:14]
    st.write("**:green[{} 현재 누적 방문자수:{}명]**".format(now, visitors - 1))
    
    

# 6.한국인 체형
if option == "예제1:Korean Body Shape":
    df_body = pd.read_csv("height.csv")

    if graph_btn:
        st.subheader("**한국인 성별 연령별 체형 정보 (통계청, 2022년 자료)**")
        st.write("**성별 연령대 평균 신장**")
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
        st.subheader("**한국인 체형 정보 (통계청, 2022년 자료)**")
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
        st.subheader("**한국 가계 경제 지표 (한국은행, 2022~2024년 자료)**")
        st.dataframe(data = df, hide_index = True,
                     width = 600, height = 550,
                     column_config={"year":st.column_config.NumberColumn(format="%d")})
    
    elif graph_btn:
        fig = plt.figure(figsize = (8, 6))
        # fig.set_facecolor("#2F2E2E")
        st.subheader("**월별 가계 경제 지표 추이 (한국은행, 2022~2024년 자료)**")
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
        st.subheader("**한국 가계 경제 지표 (한국은행, 2022~2024년 자료)**")
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
    now = dt.datetime.now(ZoneInfo("Asia/Seoul")).strftime("%y/%m/%d %H:%M")
    df = pd.read_csv("real_time_weather.csv")
    df = df.iloc[0:, 1:]
    if graph_btn:
        fig = plt.figure(figsize = (8, 6))
        # fig.set_facecolor("#2F2E2E")
        st.subheader("**전국 주요 도시 온도/습도 (기상청, RSS 서비스)**")
        st.write("**현재시각:{}**".format(now))
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
        st.subheader("**전국 주요 도시 기상 정보 (기상청, RSS 서비스)**")
        st.write("**현재시각:{}**".format(now))
        st.dataframe(data = df, use_container_width = True,
                    hide_index = True)
    else:
        st.subheader("**전국 주요 도시 기상 정보 (기상청, RSS 서비스)**")
        st.write("**현재시각:{}**".format(now))
        st.dataframe(data = df, use_container_width = True,
                    hide_index = True)

#--------------------------------------------------------------#    
# 9. 공정 능력 분석(PCI)
if option == "예제4:Process Capability":
    with st.sidebar:
        st.write("---")
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
        start = st.button(label = "공정능력 산출")

    # visualization
    y = np.random.normal(mean, stdev, 10000)
    data = norm(loc = 0.0, scale = 1.0)
    x = np.linspace(start = np.min(y), stop = np.max(y), num = 10000)
    y1 = norm.pdf(x, mean, stdev)
    if start:
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
    
        fig = plt.figure(figsize = (8, 6))
        plt.plot(x, y1, marker = "", color = "blue", linewidth = 3) 
        plt.hist(x = y, bins = 50, color = "orange", alpha = 0.7, density = True,
                 edgecolor = "black")                         
        plt.grid(True)                                               
        plt.text(x = mean*1.02, y = 0.39, s = "Process Capability(Z):{:.2f}".format(pci),
                color = "red", fontdict={"style":"italic", "size":12})
        plt.text(x = mean*1.02, y = 0.37, s = "Expected Defective:{:.0f}ppm".format(prob), 
                color = "red", fontdict={"style":"italic", "size":12})
        if type == "단측:USL":
            plt.vlines(x = [mean, usl], ymin = 0.0, ymax = 0.45, 
                       colors = ["blue", "red"], linestyles = ["dashed", "solid"],
                       label = ["Mean", "USL"])
            plt.text(x = usl, y = 0.45, s = "USL", 
                     color = "red", fontdict={"style":"italic", "size":12})
            plt.text(x = mean, y = 0.45, s = "Mean", 
                     color = "blue", fontdict={"style":"italic", "size":12})
            plt.xlim((np.min(x)-(abs(np.min(x))*0.05), usl+(abs(usl)*0.05)))
        elif type == "단측:LSL":
            plt.vlines(x = [lsl, mean], ymin = 0.0, ymax = 0.45, 
                       colors = ["red", "blue"], linestyles = ["solid", "dashed"])
            plt.text(x = lsl, y = 0.45, s = "LSL", 
                     color = "red", fontdict={"style":"italic", "size":12})
            plt.text(x = mean, y = 0.45, s = "Mean", 
                     color = "blue", fontdict={"style":"italic", "size":12})
            plt.xlim((lsl-(abs(lsl)*0.05), np.max(x)+(abs(np.max(x))*0.05)))
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
        plt.xlabel("Values Expected", color = "black", fontdict={"size":13})
        plt.ylabel("Probability", color = "black", fontdict={"size":13})
        plt.yticks(color = "black", size = 10)
        plt.xticks(color = "black", size = 10)
        plt.gca().spines["bottom"].set_visible(False)
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["left"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        st.pyplot(fig)
    else:
        st.markdown(":green[Spec., 평균, 표준편차]를 입력하세요")
        st.markdown(":green[공정 능력 산출 버튼]을 클릭하세요")
            
#--------------------------------------------------------------#       
# 10. Newspaper Crawling
if option == "예제5:Newspaper Crawling":
    # 10-1.페이지 타이틀 및 서브 타이틀
    st.title("네이버 뉴스 크롤링")             # 웹페이지의 타이틀
    st.header("실시간 뉴스 Headline 살펴보기") # 웹페이지의 헤더
    now = datetime.datetime.now(ZoneInfo("Asia/Seoul")).strftime("%y/%m/%d %H:%M") # 현재 날짜와 시각
    st.subheader("날짜:{}".format(now)) # 웹페이지 서브헤더에 날짜와 시각 출력하기
    st.markdown("---")                  # 경계선 생성

    # 10-2.뉴스 기사 크롤링 함수
    def naver_news():                                         # 함수정의 : 함수명 naver_news
        # part1. 네이버에서 뉴스 기사 스크랩핑
        now = datetime.datetime.now(ZoneInfo("Asia/Seoul"))   # 현재 날짜와 시각 객체 now 생성
        date = now.strftime("%Y%m%d")                         # 날짜와 시각 형식을 "년/월/일"로 전환
        ## 뉴스 크롤링하려는 사이트 주소를 url에 입력
        url = "https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=001&listType=title&date={}".format(date)
        ## 크롤링 대상 사이트에서 일정한 형식으로 크롤링을 위해 user-agent생성
        headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
        response = requests.get(url, headers = headers) # url에 웹페이지 code를 요청
        html = response.text                            # 웹페이지 code중에서 텍스트만 선별
        soup = BeautifulSoup(html, "html.parser")       # html parser로 html만 soup에 반환

        ## HTML구조에서 뉴스 기사가 있는 곳까지 경로를 추종하여 a태그 하위의 html을 titles에 반환
        titles = soup.select("#main_content > div.list_body.newsflash_body > ul > li > a")
        news_titles = []                                # 빈 리스트 news_titles생성
        for title in titles:                            # titles에서 title로 구성요소 전달                   
            news_titles.append(title.text)              # title의 텍스텍 요소를 news_titles저장

        # part2.동일한 뉴스 기사 제거 : 뉴스 정제
        news_titles = list(set(news_titles))            # 중복되는 news titles를 제거
        index = []                                      # 빈 리스트 index 생성
        news = []                                       # 빈 리스트 news 생성
        
        # part3.정제된 최종 뉴스와 인덱스 빈 리스트에 저장
        for i, article in enumerate(news_titles):       # news_titles에 구성요소를 aritcle에 전달
            index.append(i+1)                           # 인덱스i는 리스트index에 추가
            news.append(article)                        # 기사article은 리스트 article에 추가
            
        # part4.데이터 프레임 생성
        df = pd.DataFrame({
            "No.":index, "Articles":news})              # 리스트 index와 article로 데이터프레임 생성
        
        return df                                       # 데이터 프레임을 반환


    # 10-3.Page Layout설계
    col1, col2 = st.columns([2, 8])                     # 페이지 Layout를 2개의 Column으로 분할

    # 10-4.col1 설계                       
    with col1:                                          
        button1 = st.button(label = "뉴스 크롤링",      # button1 생성 : 레이블("뉴스 크롤링")
                            use_container_width = True)
        button2 = st.button(label = "뉴스 보기",        # button2 생성 : 레이블("뉴스 보기")
                            use_container_width = True)
        button3 = st.button(label = "워드 클라우드",    # button3 생성 : 레이블("워드 클라우드")
                            use_container_width=True)

    # 10-5.col2 설계
    with col2:
        if button1:                                     # button1을 누르면
            df = naver_news()                           # naver_news()함수 실행하여 df를 반환받음
            st.session_state["df"] = df
            
        if button2:                                     # button2를 누르면
            if "df" in st.session_state:
                st.dataframe(data = st.session_state["df"],                     # 데이터 프레임 생성
                            use_container_width = True, # 데이터는 df를 사용
                            hide_index = True)          # 폭은 현재 컨테이너 넓이 적용, 인덱스는 생략
            else:
                st.warning("[뉴스크롤링] 버튼을 눌러서 뉴스 데이터를 호출하세요!")
        
        if button3:
            df = st.session_state["df"]
            kiwi = Kiwi()
            words = []
            text = " ".join(df["Articles"].dropna())
            tokens = kiwi.tokenize(text)
            for sentence in df['Articles'].dropna():
                tokens = kiwi.tokenize(sentence)
                nouns = [token.form for token in tokens if token.tag.startswith('NN')]  # 명사만 추출
                words.extend([w for w in nouns if len(w) > 1])
            word_freq = Counter(words)
            wordclound = WordCloud(font_path="NanumGothic.ttf",
                                width = 800, height = 400, background_color="white")\
                                .generate_from_frequencies(word_freq)
            fig = plt.figure()
            plt.imshow(wordclound, interpolation="bilinear")
            plt.axis("off")
            # plt.title("주요 뉴스 WordCloud")
            st.pyplot(fig)

            
#--------------------------------------------------------------# 
# 11. Image 살펴보기
if option == "예제6:Beautiful Korea":
    # 1.이미지 폴더 경로 설정
    IMAGE_FOLDER = r"C:\Users\npain\Desktop\Python\DataAnalysis\images10/"  # 'images' 폴더 안에 이미지 파일들을 저장하세요
    image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
    image_files.sort()
    
    # 세션 상태로 이미지 인덱스 저장
    if 'img_index' not in st.session_state:
        st.session_state.img_index = 0
    
    # UI
    st.title("한국의 풍경")
    st.write("총 이미지 수: ", len(image_files))
    
    
    # 현재 이미지 표시
    if image_files:
        loaded_image = Image.open(os.path.join(IMAGE_FOLDER, image_files[st.session_state.img_index]))
        current_image = loaded_image.resize((1280, 700))
        st.image(current_image, caption=image_files[st.session_state.img_index], use_container_width=True)
    
        # 버튼 클릭 플래그 초기화
        if 'go_next' not in st.session_state:
            st.session_state.go_next = False
        if 'go_prev' not in st.session_state:
            st.session_state.go_prev = False
    
        # 버튼 배치
        col1, col2, col3 = st.columns([1, 6, 1])
        with col1:
            if st.button("◀ 이전"):
                if st.session_state.img_index > 0:
                    st.session_state.img_index -= 1
        with col3:
            if st.button("다음 ▶"):
                if st.session_state.img_index < len(image_files) - 1:
                    st.session_state.img_index += 1
    else:
        st.warning("이미지가 없습니다. 'images' 폴더에 이미지를 넣어주세요.")
    
