import os

import streamlit as st
from dotenv import load_dotenv
from revChatGPT.V1 import Chatbot

load_dotenv()

token = os.environ.get("access_token")
print(11, token)

chatbot = Chatbot(config={
    "access_token": token,
})


def chatgpt_rev(question:str)->str:
    response = ""

    for data in chatbot.ask(
            question
    ):
        response = data["message"]

    return response

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

question_text_area = st.text_area('🤖 Ask Any Question :', placeholder='Explain quantum computing in 50 words')
if st.button('🧠 Think'):
    answer = chatgpt_rev(question_text_area)
    st.caption("Answer :")
    st.markdown(answer)


hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 