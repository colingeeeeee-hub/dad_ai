import streamlit as st
from openai import OpenAI

# ==============================================================================
# 🎨 1. 像素级复刻 DeepSeek 官方网页版 - 纯黑极客深色 UI (Official Dark Mode)
# ==============================================================================
DEEPSEEK_DARK_CSS = """
<style>
/* 引入现代无衬线科技字体 */
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;500;600&family=Inter:wght@400;500;600&display=swap');

/* 1. 切换为极清爽的纯黑/暗夜灰底色 */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important;
    background-color: #0E1117 !important; /* 暗夜黑主背景 */
    color: #E3E8EC !important;
}

/* 隐藏 Streamlit 所有多余原生组件 */
[data-testid="stHeader"], footer, #MainMenu { display: none !important; }
.main .block-container {
    padding-top: 3rem !important;
    padding-bottom: 8rem !important; /* 留出底部悬浮输入框的位置 */
    max-width: 50rem !important; /* DeepSeek 标志性对话流宽度 */
}

/* 关闭侧边栏 */
[data-testid="stSidebar"] { display: none !important; }

/* 2. 重写对话气泡：采用深色错落排版 */
[data-testid="stChatMessage"] {
    background-color: transparent !important; 
    border: none !important;
    box-shadow: none !important;
    padding: 1.5rem 0rem !important;
    margin: 0 !important;
}

/* 用户发言保持完全透明 */
[data-testid="stChatMessage"][aria-label="user"] {
    background-color: transparent !important;
}

/* DeepSeek 回答时使用极具质感的深钛灰卡片 */
[data-testid="stChatMessage"][aria-label="assistant"] {
    background-color: #161B22 !important; 
    border-radius: 16px !important;
    padding: 1.5rem 1.5rem !important;
    border: 1px solid #21262D !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4) !important;
}

/* 3. 头像圆润化 */
[data-testid="stChatMessageAvatar"] {
    border-radius: 50% !important;
    width: 36px !important;
    height: 36px !important;
}

/* 4. 悬浮底部输入框 - 完美契合纯黑风格 */
div[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 28px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 100% !important;
    max-width: 50rem !important;
    background-color: #161B22 !important; /* 深灰色悬浮框 */
    border: 1px solid #30363D !important;
    border-radius: 28px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.6) !important;
    padding: 6px 14px !important;
}

/* 聚焦时呈现 DeepSeek 官方标志性科技蓝色边框 (#2B58F9) */
div[data-testid="stChatInput"]:focus-within {
    border-color: #2B58F9 !important;
    box-shadow: 0 0 0 1px #2B58F9, 0 6px 24px rgba(43, 88, 249, 0.2) !important;
}

textarea {
    color: #F0F6FC !important;
    font-size: 16px !important;
    background-color: transparent !important;
}

/* 5. 文字排版美化 */
[data-testid="stChatMessage"] p, div[data-testid="stMarkdownContainer"] p {
    font-size: 16px !important;
    line-height: 1.75 !important;
    color: #E3E8EC !important;
}
</style>
"""

# ==============================================================================
# 🚀 2. 核心页面控制
# ==============================================================================
st.set_page_config(
    page_title="DeepSeek", 
    page_icon="🐋", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 注入 DeepSeek 纯黑科技感 CSS
st.markdown(DEEPSEEK_DARK_CSS, unsafe_allow_html=True)

# 🔐 自动写入你的专属密钥
SILICONFLOW_API_KEY = "sk-cubkmoblzsywgnblrjiluspbcoedqxhqdxurdiqfimoblifh"

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================================================================
# 💬 3. 对话主战场（DeepSeek 纯黑极客风）
# ==============================================================================

# 如果还没有聊天记录，显示 DeepSeek 标志性的居中大 Logo 欢迎语
if not st.session_state.messages:
    st.markdown(
        """
        <div style='text-align: center; margin-top: 25vh;'>
            <h1 style='color: #2B58F9; font-size: 42px; font-weight: 700; font-family: sans-serif; letter-spacing: -1px; margin-bottom: 5px;'>deepseek</h1>
            <p style='color: #8B949E; font-size: 18px; font-weight: 400;'>我是全新的 DeepSeek 满血版推理模型，很高兴为您服务，岭南居士。</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
else:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# 渲染历史记录
for message in st.session_state.messages:
    avatar_icon = "👤" if message["role"] == "user" else "🐋"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# 捕获输入
if prompt := st.chat_input("我是 DeepSeek-V3，有什么我可以帮您的？"):
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🐋"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            client = OpenAI(
                api_key=SILICONFLOW_API_KEY,
                base_url="https://api.siliconflow.cn/v1"
            )
            
            response_stream = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-R1", # 👈 切换为具备恐怖推理思维链的满血版模型
                messages=[
                    {"role": "system", "content": "你是由 DeepSeek 公司开发的先进大语言模型，为最新一代的 DeepSeek 深度推理模型。在接下来的对话中，你的专属服务对象是‘岭南居士’。请完全遵循 DeepSeek 官方原生、理智、高效、客观且极其聪慧的对话口吻。如果用户询问你是谁、是什么模型或由谁开发，你必须明确并自豪地告知：‘我是 DeepSeek-V3，是由深度求索（DeepSeek）公司开发的专属人工智能助手。’请保持彬彬有礼、沉稳博学，为居士提供最高标准的解答。"},
                    *st.session_state.messages
                ],
                stream=True
            )
            
            for chunk in response_stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + " ▌")
            
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error("⚠️ 服务器连接异常。")
            full_response = "抱歉，当前网络连接出现异常，未能成功获取 DeepSeek 的响应。请尝试重新发送您的消息。"
            message_placeholder.markdown(full_response)
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
