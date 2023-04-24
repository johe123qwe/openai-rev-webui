# openai-rev-webui

![screen](image/GUI.png)

## 使用方法
1. 登陆[chatgpt](https://chat.openai.com/)
2. 打开[chatgpt-session](https://chat.openai.com/api/auth/session)， 获取 **accessToken**
3. cp .env.example .env
4. 把 "YOUR_TOKEN" 替换成你的 "accessToken"
5. pip install -r requirement.txt
6. streamlit run streamlit_app.py
