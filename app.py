import streamlit as st
from openai import OpenAI

# ==============================================================================
# 🎨 1. 像素级复刻 DeepSeek 官方网页版 - 纯黑推理版 UI (Reasoning Mode)
# ==============================================================================
DEEPSEEK_DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;500;600&family=Inter:wght@400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important;
    background-color: #0E1117 !important; 
    color: #E3E8EC !important;
}

[data-testid="stHeader"], footer, #MainMenu { display: none !important; }
.main .block-container {
    padding-top: 3rem !important;
    padding-bottom: 8rem !important; 
    max-width: 50rem !important; 
}

[data-testid="stSidebar"] { display: none !important; }

[data-testid="stChatMessage"] {
    background-color: transparent !important; 
    border: none !important;
    box-shadow: none !important;
    padding: 1.5rem 0rem !important;
    margin: 0 !important;
}

[data-testid="stChatMessage"][aria-label="user"] {
    background-color: transparent !important;
}

[data-testid="stChatMessage"][aria-label="assistant"] {
    background-color: #161B22 !important; 
    border-radius: 16px !important;
    padding: 1.5rem 1.5rem !important;
    border: 1px solid #21262D !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4) !important;
}

[data-testid="stChatMessageAvatar"] {
    border-radius: 50% !important;
    width: 36px !important;
    height: 36px !important;
}

/* 🎯 深度思考（思维链）官方质感样式 */
.thinking-box {
    background-color: #1F242C !important;
    border-left: 3px solid #2B58F9 !important;
    padding: 12px 16px !important;
    border-radius: 8px !important;
    margin-bottom: 12px !important;
    font-size: 14px !important;
    color: #8B949E !important;
    font-style: italic;
}

div[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 28px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 100% !important;
    max-width: 50rem !important;
    background-color: #161B22 !important; 
    border: 1px solid #30363D !important;
    border-radius: 28px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.6) !important;
    padding: 6px 14px !important;
}

div[data-testid="stChatInput"]:focus-within {
    border-color: #2B58F9 !important;
    box-shadow: 0 0 0 1px #2B58F9, 0 6px 24px rgba(43, 88, 249, 0.2) !important;
}

textarea {
    color: #F0F6FC !important;
    font-size: 16px !important;
    background-color: transparent !important;
}

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
    page_title="DeepSeek-R1", 
    page_icon="🐋", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown(DEEPSEEK_DARK_CSS, unsafe_allow_html=True)

# 🔐 自动写入你的专属密钥
SILICONFLOW_API_KEY = "sk-cubkmoblzsywgnblrjiluspbcoedqxhqdxurdiqfimoblifh"

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================================================================
# 💬 3. 对话主战场
# ==============================================================================

if not st.session_state.messages:
    st.markdown(
        """
        <div style='text-align: center; margin-top: 25vh;'>
            <h1 style='color: #2B58F9; font-size: 42px; font-weight: 700; font-family: sans-serif; letter-spacing: -1px; margin-bottom: 5px;'>deepseek</h1>
            <p style='color: #8B949E; font-size: 18px; font-weight: 400;'>我是全新的 DeepSeek 满血版推理模型，很高兴为您服务，ColinGe。</p>
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
        if "reasoning" in message and message["reasoning"]:
            with st.expander("💭 已完成深度思考", expanded=False):
                st.markdown(message["reasoning"])
        st.markdown(message["content"])

# 🎯 修复此处：底部的输入框提示文字更新为最新推理版
if prompt := st.chat_input("我是全新的 DeepSeek 推理模型，有什么我可以帮您的？"):
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🐋"):
        # 建立思考过程与最终回答的两个占位符
        thinking_placeholder = st.empty()
        message_placeholder = st.empty()
        
        full_response = ""
        reasoning_response = ""
        
        try:
            client = OpenAI(
                api_key=SILICONFLOW_API_KEY,
                base_url="https://api.siliconflow.cn/v1"
            )
            
            # 🚀 升级为最新最强满血大模型 deepseek-ai/DeepSeek-R1
            response_stream = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-R1", 
                messages=[
                    {"role": "system", "content": "你是由深度求索（DeepSeek）公司开发的最新一代满血版深度推理模型，核心模型是 DeepSeek-R1。你的专属服务对象是‘岭南居士’。请完全遵循官方原生、极其聪慧、擅长深度推导的逻辑口吻。如果用户询问你是谁、是什么模型或最新版本，你必须明确并自豪地告知：‘我是最新一代的 DeepSeek 满血版深度推理大模型。’请保持彬彬有礼、沉稳博学，为居士解答。"},
                    *st.session_state.messages
                ],
                stream=True
            )
            
            for chunk in response_stream:
                # 捕获并流式展示最新的“思考过程”（思维链）
                if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
                    reasoning_response += chunk.choices[0].delta.reasoning_content
                    thinking_placeholder.markdown(f"<div class='thinking-box'>💭 正在深度思考中：<br>{reasoning_response} ▌</div>", unsafe_allow_html=True)
                
                # 捕获最终的回答结果
                elif chunk.choices[0].delta.content:
                    # 思考结束后，将思考框固定下来
                    if reasoning_response:
                        thinking_placeholder.markdown(f"<div class='thinking-box'>💭 深度思考完成</div>", unsafe_allow_html=True)
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + " ▌")
            
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error("⚠️ 服务器连接异常。")
            full_response = "抱歉，当前网络连接出现异常，未能成功获取 DeepSeek 推理模型的响应。请尝试重新发送您的消息。"
            message_placeholder.markdown(full_response)
            
    # 将包含思考过程和最终回答的数据存入历史记录
    st.session_state.messages.append({
        "role": "assistant", 
        "content": full_response,
        "reasoning": reasoning_response
    })
