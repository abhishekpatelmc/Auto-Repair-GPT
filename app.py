import streamlit as st
import openai
import os

# Set page config
openApiKey = st.secrets["OPENAI_API_KEY"]

# Set Sidebar
with st.sidebar:
    st.title('🔧 Auto Repair GPT')
    st.write(
        'This app uses the OpenAI GPT-3 API to generate text based on user input.')

# Set page title
st.title('💬 Auto Repair GPT App')
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openApiKey:
        st.info("OpenAI API Not working...")
        st.stop()

    openai.api_key = openApiKey
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("Auto-GPT").write(msg.content)
