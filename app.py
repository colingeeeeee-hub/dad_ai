import streamlit as st
from openai import OpenAI

# ==============================================================================
# 🎨 1. 像素级复刻 ChatGPT 网页版 UI (The Ultimate Custom CSS)
# ==============================================================================
PERFECT_CHATGPT_CSS = """
<style>
/* 引入 ChatGPT 官方同款 Söhne/Inter 字体 */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

/* 1. 彻底抹平 Streamlit 原生布局与边距 */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    background-color: #212121 !important; /* ChatGPT 官方主背景深色 */
    color: #ECECF1 !important;
}

/* 隐藏所有多余的垃圾元素：顶部红线、Header 空白、Footer、右上角菜单 */
[data-testid="stHeader"], footer, #MainMenu { display: none !important; }
.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 7rem !important; /* 留出底部输入框的悬浮空间 */
    max-width: 48rem !important; /* ChatGPT 标志性的对话流宽度 (768px) */
}

/* 2. 彻底关闭侧边栏 */
[data-testid="stSidebar"] { display: none !important; }

/* 3. 彻底重写对话气泡：去掉方框感，改用 ChatGPT 无框横条流式布局 */
[data-testid="stChatMessage"] {
    background-color: transparent !important; /* 全部透明 */
    border: none !important;
    box-shadow: none !important;
    padding: 1.5rem 0rem !important;
    margin: 0 !important;
    border-bottom: 1px solid #2F2F2F !important; /* 淡淡的分割线 */
}

/* 4. 头像圆润化与ChatGPT配色 */
[data-testid="stChatMessageAvatar"] {
    background-color: transparent !important;
    border-radius: 50% !important; /* 完美的圆形头像 */
    width: 36px !important;
    height: 36px !important;
}

/* 5. 极致复刻：ChatGPT 悬浮底部输入框 */
div[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 24px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 100% !important;
    max-width: 48rem !important; /* 与对话流完美对齐 */
    background-color: #2F2F2F !important; /* 输入框标志性浅灰 */
    border: 1px solid #424242 !important;
    border-radius: 26px !important; /* 极致圆润 */
    box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
    padding: 6px 12px !important;
}

/* 移除输入框聚焦时的边框 */
div[data-testid="stChatInput"]:focus-within {
    border-color: #565656 !important;
}

textarea {
    color: #F4F4F4 !important;
    font-size: 16px !important;
    background-color: transparent !important;
}

/* 6. 字体美化：让大模型的字看起来充满高级印刷感 */
[data-testid="stChatMessage"] p, div[data-testid="stMarkdownContainer"] p {
    font-size: 16px !important;
    line-height: 1.75 !important;
    color: #E3E3E3 !important;
    font-weight: 400 !important;
}
</style>
"""

# ==============================================================================
# 🚀 2. 核心页面控制与样式注入
# ==============================================================================
st.set_page_config(
    page_title="岭南居士的专属人工智能", 
    page_icon="🤖", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 强制注入终极美化 CSS
st.markdown(PERFECT_CHATGPT_CSS, unsafe_allow_html=True)

# 填入你的硅基流动 API Key
SILICONFLOW_API_KEY = "sk-xxxxxxxx" # 👈 请记得把这里换成你的真实 Key

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================================================================
# 💬 3. 对话主战场
# ==============================================================================

# 如果还没有聊天记录，显示 ChatGPT 经典的居中欢迎语（已更新为居士定制版）
if not st.session_state.messages:
    st.markdown("<h2 style='text-align: center; font-weight: 600; margin-top: 30vh; color: #FFF;'>有什么我可以帮您的，岭南居士？</h2>", unsafe_allow_html=True)
else:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# 渲染历史记录
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 捕获输入
if prompt := st.chat_input("给“岭南居士的专属人工智能”发送消息..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            client = OpenAI(
                api_key="sk-cubkmoblzsywgnblrjiluspbcoedqxhqdxurdiqfimoblifh",
                base_url="https://api.siliconflow.cn/v1"
            )
            
            response_stream = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3", 
                messages=[
                    # 🤖 核心口吻重构：模仿 ChatGPT 的通用、专业、理性的智能助手口吻，并针对“岭南居士”保持礼貌尊称
                    {"role": "system", "content": "你是由高级语言模型训练而来的专属人工智能助手。在接下来的对话中，你的服务对象是‘岭南居士’。请保持类似 ChatGPT 的专业、中立、客观且逻辑清晰的谈话风格。你的语气应当彬彬有礼、沉稳博学，并具备优秀的耐心。请根据用户的输入提供准确的解答、信息检索、文学探讨或日常交流，确保回答高效且具有深度，严禁出现任何家庭或私人关系的代入感。"},
                    *st.session_state.messages
                ],
                stream=True
            )
            
            for chunk in response_stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    # ChatGPT 经典黑方块打字光标 █
                    message_placeholder.markdown(full_response + " █")
            
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error("⚠️ 网络连接似乎断开了。")
            full_response = "抱歉，当前网络连接出现异常，未能成功获取响应。请尝试重新发送您的消息。"
            message_placeholder.markdown(full_response)
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
