import json
import os
import random
import string

import jieba
import jieba.analyse
import streamlit as st
from dotenv import load_dotenv
from revChatGPT.V1 import Chatbot

load_dotenv()

token = os.environ.get("access_token")

# 设置停用词
jieba.analyse.set_stop_words('stopwords.txt')

chatbot = Chatbot(config={
    "access_token": token,
})

def read_json():
    with open('./data/data.json') as f:
        data = json.load(f)
    return data

def write_json(data):
    with open('./data/data.json', 'w') as f:
        json.dump(data, f, indent=4)

def chatgpt_rev(question:str)->str:
    response = ""

    for data in chatbot.ask(
            question
    ):
        response = data["message"]

    return response

def search_jieba(key):
    seg_list = jieba.analyse.extract_tags(key, topK=20, withWeight=False, allowPOS=())
    results = []
    for item in seg_list:
        result = search_data(read_json(), item, item)
        for i in result:
            results.append(i)
    return list(set(results))


def generate_random_code(length):
    # 生成包含小写字母和数字的字符集
    characters = string.ascii_lowercase + string.digits
    # 随机选择 length 个字符并将其组合起来
    code = ''.join(random.choices(characters, k=length))
    return code

def search_json(obj, key, value):
    results = []
    if isinstance(obj, dict):
        if key in obj and obj[key] == value:
            results.append(obj)
        for sub_obj in obj.values():
            results += search_json(sub_obj, key, value)
    elif isinstance(obj, list):
        for sub_obj in obj:
            results += search_json(sub_obj, key, value)
    return results

def search_data(data, key, value):
    results = []
    for item in data.items():
        for k, v in item[1].items():
            if k.strip('\n') == key:
                results.append(item[1][k])
            if value in v.strip('\n'):
                results.append(item[1][k])
    return results

def make_results(my_list):
    results = ''
    for index in range(0, len(my_list)):
        if my_list[index] != '':
            results += '⭐' + '  ' + my_list[index].strip('\n') + '\n\n\n'
    return results

st.set_page_config(
    page_title="openaiGUI",
    initial_sidebar_state="expanded",
    page_icon="🧠",
    menu_items={
        'Get Help': 'https://github.com/johe123qwe/openai-rev-webui/main/README.md',
        'About': "### gptweb GUI"
    }
)

st.header('GPT GUI')

lixian = ''
search_key = ''
if st.checkbox('离线搜索'):
    lixian = 'lixian'

if st.checkbox('精确搜索'):
    search_key = 'jingque'

question_text_area = st.text_area('🤖 Ask Any Question :', placeholder='Explain quantum computing in 50 words')
if st.button('🧠 Think'):
    if lixian != 'lixian':
        answer = chatgpt_rev(question_text_area)
        code = generate_random_code(20)
        dic = {}
        data = read_json()
        dic[question_text_area] = answer
        data[code] = dic
        write_json(data)
    else:
        answer = ''
    if search_key == 'jingque':
        results_his = search_data(read_json(), question_text_area, question_text_area)
    else:
        results_his = search_jieba(question_text_area)
    results_hiss = make_results(results_his)
    st.caption("Answer :")
    st.markdown(answer + '\n\n### 📝本地记录 :\n\n' + results_hiss)


hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 