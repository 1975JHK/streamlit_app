# 1.필요한 라이브러리 호출
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import random, time

# 2.페이지 제목 설정
st.set_page_config(
    page_title="로또 번호 생성기",
    page_icon="💰",
    layout="wide"
)

# 3.제목과 헤드 작성
st.title(body="로또 번호 생성기")
st.header(":slot_machine:로또 번호 손쉬게 작성하자!!")
st.subheader(body=":date:작성일자:2023/2/4")

# 4.로또 번호 생성 함수
def lotto_generator():
    lotto_nums = None
    lotto_nums = random.sample(range(1, 46), k=6)
    return lotto_nums

# 5.로또 번호 생성 실행
st.markdown("---")
st.markdown("**:green[로또 번호]를 자동 생성합니다!**")
button = st.button(
    label = "번호 생성")

if button:
    nums = lotto_generator()
    nums.sort(reverse=False)
    for i in range(6):
        st.write("[{}]번째 :green[행운숫자]:{}".format(i+1, nums[i]))
        time.sleep(1)
    st.markdown(body="*행운의 로또번호:{}*".format(nums))
