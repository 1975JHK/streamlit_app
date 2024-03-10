# 1.필요한 라이브러리 호출
import streamlit as st
import numpy as np
import pandas as pd
import datetime as dt

# 2.페이지 기본 설정
st.set_page_config(
page_title = "EDA")

# 3.페이티 제목 및 Header
st.title("Exploratory Data Analysis with Streamlit")
st.header("First Web App with Streamlit")
st.subheader("Date and Time : {}".format(dt.datetime.now().strftime("%y/%m/%d %H:%M")))
