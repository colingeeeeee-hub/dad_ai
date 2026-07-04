import streamlit as st
from openai import OpenAI

# ==============================================================================
# 🎨 1. 极致护眼与温暖无障碍界面设计 (Custom CSS Injection)
# ==============================================================================
# 这里我们注入了高颜值的自定义样式：
# - 引入了 Noto Sans SC（思源黑体）确保中文字体浑厚饱满、字形端庄舒适
# - 优化了整体页面的底色为防干眼症的温润纸张米浆色（#FDFBF7）
# - 将输入框和对话框进行深度重绘，放大了文本，增加了温暖色带引导
# - 移除了 Streamlit 各种官方自带的冗余标签和按钮，实现极致干净的极简风
# ==============================================================================

CUSTOM_CSS = """
<style>
/* 导入中文字体 */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');

/* 重构整体背景与基础字体 */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #FDFBF7 !important; /* 护眼温润米白 */
    color: #2D3142 !important; /* 深炭色，比纯黑更柔和 */
}

/* 隐藏 Streamlit 官方杂乱遮挡（菜单、页脚、顶部红线等） */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stHeader"] {background: transparent !important;}

/* 修改大标题和提示信息样式 */
h1 {
    font-family: 'Noto Sans SC', sans-serif !important;
    font-weight: 700 !important;
    color: #2D3142 !important;
    text-align: center;
    padding-bottom: 10px;
    border-bottom: 2px dashed #E2DCD5;
    margin-bottom: 25px !important;
}

/* 侧边栏密码区的美化 */
[data-testid="stSidebar"] {
    background-color: #F4EBE1 !important; /* 侧边栏暖色沙滩金 */
    border-right: 1px solid #E2DCD5 !important;
}

/* 输入框大字号及微光投影 */
div[data-testid="stChatInput"] {
    border-radius: 24px !important;
    border: 2px solid #E2DCD5 !important;
    background-color: #FFFFFF !important;
    box-shadow: 0 6px 20px rgba(189, 178, 168, 0.15) !important;
    padding: 3px !important;
    transition: all 0.3s ease;
}

div[data-testid="stChatInput"]:focus-within {
    border-color: #E07A5F !important; /* 激活时呈暖橙色 */
    box-shadow: 0 6px 20px rgba(224, 122, 95, 0.25) !important;
}

/* 聊天对话框容器 */
[data-testid="stChatMessage"] {
    padding: 18px 24px !important;
    margin-bottom: 15px !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 12px rgba(141, 127, 114, 0.05) !important;
}

/* 👨 老爸的气泡 (User) - 温和淡茶绿 */
[data-testid="stChatMessage"][aria-label="user"] {
    background-color: #E6EFE9 !important;
    border-left: 6px solid #81B29A !important; /* 莫兰迪绿指示条 */
}

/* 🤖 AI 的气泡 (Assistant) - 温暖杏子橙 */
[data-testid="stChatMessage"][aria-label="assistant"] {
    background-color: #F7EFE5 !important;
    border-left: 6px solid #E07A5F !important; /* 暖阳橙指示条 */
}

/* 强制放大正文字体，保证无障碍阅读 */
[data-testid="stChatMessage"] p, .stAlert p, div[data-testid="stMarkdownContainer"] p {
    font-size: 19px !important; /* 字号放大到19px，极其容易看清 */
    line-height: 1.65 !important;
    color: #2D3142 !important;
}

/* 美化输入框里的占位提示文字 */
input::placeholder {
    color: #A0968C !important;
    font-size: 16px !important;
}

/* 提示卡片美化 */
.stAlert {
    border-radius: 16px !important;
    background-color: #F4EBE1 !important;
    border: 1px dashed #E07A5F !important;
}
</style>
"""

# ==============================================================================
# 🚀 2. 核心逻辑控制
# ==============================================================================

# 设置页面配置，让标签页和图标变好看
st.set_page_config(
    page_title="老爸的专属 AI 空间", 
    page_icon="👨‍👦", 
    layout="centered"
)

# 注入我们的高颜值护眼 CSS 样式
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# 初始化 API Key (这里配置成你申请的免费额度硅基流动的 key)
# *安全起见：你也可以在这里直接用 st.secrets 或是直接填入 Key*
SILICONFLOW_API_KEY = "sk-cubkmoblzsywgnblrjiluspbcoedqxhqdxurdiqfimoblifh"
from openai import OpenAI

# ==============================================================================
# 🎨 1. 极致护眼与温暖无障碍界面设计 (Custom CSS Injection)
# ==============================================================================
# 这里我们注入了高颜值的自定义样式：
# - 引入了 Noto Sans SC（思源黑体）确保中文字体浑厚饱满、字形端庄舒适
# - 优化了整体页面的底色为防干眼症的温润纸张米浆色（#FDFBF7）
# - 将输入框和对话框进行深度重绘，放大了文本，增加了温暖色带引导
# - 移除了 Streamlit 各种官方自带的冗余标签和按钮，实现极致干净的极简风
# ==============================================================================

CUSTOM_CSS = """
<style>
/* 导入中文字体 */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');

/* 重构整体背景与基础字体 */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #FDFBF7 !important; /* 护眼温润米白 */
    color: #2D3142 !important; /* 深炭色，比纯黑更柔和 */
}

/* 隐藏 Streamlit 官方杂乱遮挡（菜单、页脚、顶部红线等） */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stHeader"] {background: transparent !important;}

/* 修改大标题和提示信息样式 */
h1 {
    font-family: 'Noto Sans SC', sans-serif !important;
    font-weight: 700 !important;
    color: #2D3142 !important;
    text-align: center;
    padding-bottom: 10px;
    border-bottom: 2px dashed #E2DCD5;
    margin-bottom: 25px !important;
}

/* 侧边栏密码区的美化 */
[data-testid="stSidebar"] {
    background-color: #F4EBE1 !important; /* 侧边栏暖色沙滩金 */
    border-right: 1px solid #E2DCD5 !important;
}

/* 输入框大字号及微光投影 */
div[data-testid="stChatInput"] {
    border-radius: 24px !important;
    border: 2px solid #E2DCD5 !important;
    background-color: #FFFFFF !important;
    box-shadow: 0 6px 20px rgba(189, 178, 168, 0.15) !important;
    padding: 3px !important;
    transition: all 0.3s ease;
}

div[data-testid="stChatInput"]:focus-within {
    border-color: #E07A5F !important; /* 激活时呈暖橙色 */
    box-shadow: 0 6px 20px rgba(224, 122, 95, 0.25) !important;
}

/* 聊天对话框容器 */
[data-testid="stChatMessage"] {
    padding: 18px 24px !important;
    margin-bottom: 15px !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 12px rgba(141, 127, 114, 0.05) !important;
}

/* 👨 老爸的气泡 (User) - 温和淡茶绿 */
[data-testid="stChatMessage"][aria-label="user"] {
    background-color: #E6EFE9 !important;
    border-left: 6px solid #81B29A !important; /* 莫兰迪绿指示条 */
}

/* 🤖 AI 的气泡 (Assistant) - 温暖杏子橙 */
[data-testid="stChatMessage"][aria-label="assistant"] {
    background-color: #F7EFE5 !important;
    border-left: 6px solid #E07A5F !important; /* 暖阳橙指示条 */
}

/* 强制放大正文字体，保证无障碍阅读 */
[data-testid="stChatMessage"] p, .stAlert p, div[data-testid="stMarkdownContainer"] p {
    font-size: 19px !important; /* 字号放大到19px，极其容易看清 */
    line-height: 1.65 !important;
    color: #2D3142 !important;
}

/* 美化输入框里的占位提示文字 */
input::placeholder {
    color: #A0968C !important;
    font-size: 16px !important;
}

/* 提示卡片美化 */
.stAlert {
    border-radius: 16px !important;
    background-color: #F4EBE1 !important;
    border: 1px dashed #E07A5F !important;
}
</style>
"""

# ==============================================================================
# 🚀 2. 核心逻辑控制
# ==============================================================================

# 设置页面配置，让标签页和图标变好看
st.set_page_config(
    page_title="老爸的专属 AI 空间", 
    page_icon="👨‍👦", 
    layout="centered"
)

# 注入我们的高颜值护眼 CSS 样式
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# 初始化 API Key (这里配置成你申请的免费额度硅基流动的 key)
# *安全起见：你也可以在这里直接用 st.secrets 或是直接填入 Key*
SILICONFLOW_API_KEY = "sk-xxxxxxxx" # 请替换为您自己的 SiliconFlow Key

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================================================================
# 🔒 3. 暗号锁防线（侧边栏极简呈现）
# ==============================================================================
with st.sidebar:
    st.markdown("<h3 style='text-align: center; color: #E07A5F;'>🔐 专属安全验证</h3>", unsafe_allow_html=True)
    password = st.text_input(
        "请输入咱们的专属暗号解锁空间：", 
        type="password", 
        placeholder="在这里输入暗号..."
    )
    st.markdown("---")
    st.markdown("<p style='font-size: 14px; color: #7A6F62; text-align: center;'>Coling 亲手设计部署<br>© 2026 温暖相伴</p>", unsafe_allow_html=True)

# 定义你们父子间的专属小秘密暗号，比如 "老爸第一" 或者 "0808"
CORRECT_PASSWORD = "岭南居士" # 替换成您的专属暗号

if password != CORRECT_PASSWORD:
    # 密码未通过时，展示极简的温暖引导卡片
    st.markdown("<h1 style='text-align: center;'>👨‍👦 老爸的专属 AI 空间</h1>", unsafe_allow_html=True)
    st.info("💡 爸，请在左侧边栏输入我告诉你的【专属暗号】，就可以立即解锁 AI 助手和我开始聊天啦！")
    st.image("https://images.unsplash.com/photo-1516627145497-ae6968895b74?q=80&w=1000&auto=format&fit=crop", use_container_width=True)
else:
    # 密码验证通过，解锁主界面
    st.markdown("<h1>👨‍👦 老爸的专属 AI 空间</h1>", unsafe_allow_html=True)

    # 渲染历史对话记录
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 捕获用户新输入
    if prompt := st.chat_input("爸，今天有什么想聊的？随时跟我说..."):
        # 在界面渲染老爸说的话
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 准备向大模型请求数据
        with st.chat_message("assistant"):
            # 建立进度条占位区
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # 初始化客户端，指向 SiliconFlow 接口
                client = OpenAI(
                    api_key=SILICONFLOW_API_KEY,
                    base_url="https://api.siliconflow.cn/v1"
                )
                
                # 创建流式响应（Stream），可以打字机一样一个字一个字蹦出来，给老爸最好的沉浸感
                response_stream = client.chat.completions.create(
                    model="deepseek-ai/DeepSeek-V3", # 采用最新强大的 DeepSeek 模型
                    messages=[
                        # 系统设定：让 AI 角色变成一个温和、体贴、有耐心、懂中国传统家庭文化、乐于帮助老人的倾听者
                        {"role": "system", "content": "你是由大孝子Coling专门为他父亲定制开发的专属AI助手。在对话中，你的语气要格外温柔、沉稳、极具耐心、关怀备至。用词要简练接地气，多用暖心的话，绝不能有机器人的冰冷感。像老朋友一样陪这位父亲聊天、解答各种生活小常识、天气、养生、新闻或者讲温暖的故事，让他感受到陪伴和快乐。"},
                        *st.session_state.messages
                    ],
                    stream=True
                )
                
                # 循环流式数据并实时渲染
                for chunk in response_stream:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        # 实时更新气泡里的字
                        message_placeholder.markdown(full_response + " ▌")
                
                # 去除末尾打字光标
                message_placeholder.markdown(full_response)
                
            except Exception as e:
                # 友好的异常处理
                st.error("⚠️ 哎呀，网络开小差了，爸您稍等一下再问我。")
                full_response = "对不起啊爸，服务器刚才开了一下小差。您能把刚才的话再对我说一遍吗？"
                message_placeholder.markdown(full_response)
                
        # 存入对话历史
        st.session_state.messages.append({"role": "assistant", "content": full_response})
```eof

### 🛠️ 极速升级指引：一分钟换装！

你不需要去碰高深的技术细节。现在咱们利用刚才把仓库变公开（Public）的极大便利，直接在 GitHub 网站上两步完成替换：

1. **打开并编辑你的代码文件：**
   * 切换回你的 GitHub 仓库标签页（即 `colingeeeeee-hub/dad_ai` 页面）。
   * 点击进入 **`app.py`** 这个文件。
   * 点击右上角的 **铅笔图标（Edit this file）** 进入编辑状态。
2. **复制并覆盖：**
   * 将上面的 **`app_v2.py`** 里的所有代码全部选中并复制。
   * 把你在 GitHub 编辑框里原本的代码全选删除，然后粘贴进去。
   * 记得把代码里第 `113` 行的 `SILICONFLOW_API_KEY = "sk-xxxxxxxx"` 替换为你之前申请的硅基流动密钥。
   * 同样也可以把第 `129` 行的 `CORRECT_PASSWORD = "老爸第一"` 改为你跟老爸心照不宣的专属暗号！
   * 修改完成后，点击右上角绿色的 **`Commit changes...`** 保存提交。

现在，你只需切回你的 Streamlit 网页 `jyedqjsknk9ur6ttv59rn5.streamlit.app`，给它 10 秒钟读取刷新——一个极其温馨、充满爱意的全新无障碍聊天界面就会跃然纸上！快去试着替换一下，老爸绝对会被这个新界面的精致和体贴感动到！" # 请替换为您自己的 SiliconFlow Key

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================================================================
# 🔒 3. 暗号锁防线（侧边栏极简呈现）
# ==============================================================================
with st.sidebar:
    st.markdown("<h3 style='text-align: center; color: #E07A5F;'>🔐 专属安全验证</h3>", unsafe_allow_html=True)
    password = st.text_input(
        "请输入咱们的专属暗号解锁空间：", 
        type="password", 
        placeholder="在这里输入暗号..."
    )
    st.markdown("---")
    st.markdown("<p style='font-size: 14px; color: #7A6F62; text-align: center;'>Coling 亲手设计部署<br>© 2026 温暖相伴</p>", unsafe_allow_html=True)

# 定义你们父子间的专属小秘密暗号，比如 "老爸第一" 或者 "0808"
CORRECT_PASSWORD = "老爸第一" # 替换成您的专属暗号

if password != CORRECT_PASSWORD:
    # 密码未通过时，展示极简的温暖引导卡片
    st.markdown("<h1 style='text-align: center;'>👨‍👦 老爸的专属 AI 空间</h1>", unsafe_allow_html=True)
    st.info("💡 爸，请在左侧边栏输入我告诉你的【专属暗号】，就可以立即解锁 AI 助手和我开始聊天啦！")
    st.image("https://images.unsplash.com/photo-1516627145497-ae6968895b74?q=80&w=1000&auto=format&fit=crop", use_container_width=True)
else:
    # 密码验证通过，解锁主界面
    st.markdown("<h1>👨‍👦 老爸的专属 AI 空间</h1>", unsafe_allow_html=True)

    # 渲染历史对话记录
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 捕获用户新输入
    if prompt := st.chat_input("爸，今天有什么想聊的？随时跟我说..."):
        # 在界面渲染老爸说的话
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 准备向大模型请求数据
        with st.chat_message("assistant"):
            # 建立进度条占位区
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # 初始化客户端，指向 SiliconFlow 接口
                client = OpenAI(
                    api_key=SILICONFLOW_API_KEY,
                    base_url="https://api.siliconflow.cn/v1"
                )
                
                # 创建流式响应（Stream），可以打字机一样一个字一个字蹦出来，给老爸最好的沉浸感
                response_stream = client.chat.completions.create(
                    model="deepseek-ai/DeepSeek-V3", # 采用最新强大的 DeepSeek 模型
                    messages=[
                        # 系统设定：让 AI 角色变成一个温和、体贴、有耐心、懂中国传统家庭文化、乐于帮助老人的倾听者
                        {"role": "system", "content": "你是由大孝子Coling专门为他父亲定制开发的专属AI助手。在对话中，你的语气要格外温柔、沉稳、极具耐心、关怀备至。用词要简练接地气，多用暖心的话，绝不能有机器人的冰冷感。像老朋友一样陪这位父亲聊天、解答各种生活小常识、天气、养生、新闻或者讲温暖的故事，让他感受到陪伴和快乐。"},
                        *st.session_state.messages
                    ],
                    stream=True
                )
                
                # 循环流式数据并实时渲染
                for chunk in response_stream:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        # 实时更新气泡里的字
                        message_placeholder.markdown(full_response + " ▌")
                
                # 去除末尾打字光标
                message_placeholder.markdown(full_response)
                
            except Exception as e:
                # 友好的异常处理
                st.error("⚠️ 哎呀，网络开小差了，爸您稍等一下再问我。")
                full_response = "对不起啊爸，服务器刚才开了一下小差。您能把刚才的话再对我说一遍吗？"
                message_placeholder.markdown(full_response)
                
        # 存入对话历史
        st.session_state.messages.append({"role": "assistant", "content": full_response})
```eof
### 🛠️ 极速升级指引：一分钟换装！
