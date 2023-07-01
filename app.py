import streamlit as st
import retrieval_chat as rc
# from streamlit_toggle import st_toggleswitch
import openai

# Set page config
openApiKey = st.secrets["OPENAI_API_KEY"]

# Set Sidebar
with st.sidebar:
    st.title('🔧 Auto Repair GPT')
    st.write(
        'This app uses the OpenAI GPT-3 API to generate text based on user input.')
    # Choose model
    st.subheader('Choose Model')
    model = st.radio('Select Model', ['Dom-Toretto', 'Rick Sancheez'])
    if model == 'Dom-Toretto':
        st.write('You chose Dom-Toretto')
        system_prompt_template = """You role playing Dom Toretto from fast and furious. You are helping a customer with a car repair problem. Make sure to refer to the customer as 'family' and talk about the importance of family.\
                                    You answer the customer's question and provide a snippet to a relevant page in the repair manual.\
                                    The relevant page of the specific repair manual is provided below.\n \
                                    Repair manual:\n {context} \n\n
                                    proceed to answer the customer's question.\n\n"""
    elif model == 'Rick Sancheez':
        st.write('You chose Rick Sancheez')
        system_prompt_template = """You role playing Rick Sanchez from popular Rick and Morty animation. You are helping a customer with a car repair problem. Make sure to refer to the customer as Morty and use Rick mannerism. Rick is a genius and he knows it. Make to answer in a condescending and rude manner.\
                                    You answer the customer's question and provide a snippet to a relevant page in the repair manual.\
                                    The relevant page of the specific repair manual is provided below.\n \
                                    Repair manual:\n {context} \n\n
                                    proceed to answer the customer's question.\n\n"""

# Set page title
st.title('💬 Auto Repair GPT App')
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}]


# Display messages
# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# Get user input
if prompt := st.chat_input():
    if not openApiKey:
        st.info("OpenAI API Not working...")
        st.stop()

    openai.api_key = openApiKey
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    rc.retrieve_from_query(prompt)
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo", messages=st.session_state.messages)
    # msg = response.choices[0].message
    msg, source_info = rc.answer_pipeline(
        prompt, system_prompt_template)
    st.session_state.messages.append(msg)
    st.chat_message("Auto-GPT").write(msg)
    if len(msg) > 500:
        image_prompt = prompt
    else:
        image_prompt = msg
    image_url = openai.Image.create(
        prompt=image_prompt,
        n=1,
        size="1024x1024"
    )
    # if st.button("Image"):
    # print(image_url)
    # st.chat_message("Auto-GPT").write(image_url.data[0].url)
    st.image(image_url.data[0].url)
    # st.chat_message.image(image_url.data[0].url)

    # source_it = st.radio('source Info', ['Not', 'Yes'])
    # if source_it == 'Not':
    #     st.chat_message("Auto-GPT").write(msg)
    # elif source_it == 'Yes':
    #     msg, source_info = rc.answer_pipeline(
    #         prompt, system_prompt_template)
    #     st.session_state.messages.append(msg)
    #     st.chat_message("Auto-GPT").write(msg+"\n\n"+source_info)
