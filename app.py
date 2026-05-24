import streamlit as st
import streamlit.components.v1 as components
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_core.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
import PyPDF2
import os

# --- 1. Mobile-First UI Customization ---
st.set_page_config(page_title="DaruMA Galaxy AI", layout="centered")
st.markdown("""
    <style>
    .stApp { max-width: 600px; margin: 0 auto; background-color: #020617; color: #ffffff; }
    h1 { color: #22d3ee !important; text-align: center; font-size: 28px !important; }
    .stChatInput { position: fixed; bottom: 0; padding: 10px; background: #0f172a; }
    </style>
""", unsafe_allow_html=True)

# --- 2. Tools (คลังเครื่องมือ) ---
search_engine = DuckDuckGoSearchRun()

def web_builder_mock(html_code):
    st.session_state.last_html = html_code
    return "🌐 เว็บไซต์อัปเดตแล้ว ดูผลลัพธ์ในหน้า Live Preview"

tools = [
    Tool(name="Web_Search", func=search_engine.run, description="ค้นหาข้อมูล"),
    Tool(name="Web_Builder", func=web_builder_mock, description="สร้างหน้าเว็บ HTML")
]

# --- 3. Main Logic ---
st.title("🌌 DaruMA Galaxy AI")
api_key = st.text_input("Gemini API Key:", type="password")

if "last_html" not in st.session_state: st.session_state.last_html = "<h3>รอการสร้างเว็บ...</h3>"
if "messages" not in st.session_state: st.session_state.messages = []

if api_key:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_key)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, memory=memory)

    # แสดงผล
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    if prompt := st.chat_input("สั่งการ DaruMA..."):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("กำลังประมวลผลทางช้างเผือก..."):
            response = agent.run(prompt)
            st.chat_message("assistant").write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # Live Preview Section
    if st.button("ดูหน้าเว็บที่สร้าง"):
        components.html(st.session_state.last_html, height=300)

else:
    st.info("กรุณาใส่ API Key เพื่อเริ่มการใช้งาน")
ry = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, memory=memory)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("แชทกับ AI")
        if "messages" not in st.session_state: st.session_state.messages = []
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        
        if prompt := st.chat_input():
            st.chat_message("user").write(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = agent.run(prompt)
            st.chat_message("assistant").write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    with col2:
        st.subheader("Live Workspace")
        if "html_code" in st.session_state:
            components.html(st.session_state.html_code, height=400)
        else:
            st.info("สั่ง AI ให้สร้างเว็บไซต์ แล้วผลลัพธ์จะขึ้นที่นี่")
else:
    st.warning("กรุณาใส่ API Key ที่แถบด้านซ้าย")
