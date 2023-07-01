
# %%
import streamlit as st
import pinecone
import openai

# get API key from top-right dropdown on OpenAI website
openai.api_key = st.secrets["OPENAI_API_KEY"]

openai.Engine.list()  # check we have authenticated

embed_model = "text-embedding-ada-002"

# %%
# initialize connection to pinecone (get API key at app.pinecone.io)
api_key = st.secrets["PINECONE_API_KEY"]
# find your environment next to the api key in pinecone console
env = st.secrets["PINECONE_ENVIRONMENT"]

pinecone.init(api_key=api_key, environment=env)
print(pinecone.whoami())
print(pinecone.list_indexes())
index = pinecone.Index("car-repair-docs")
print(index.describe_index_stats())


# %%
query = "How do I change my oil?"


def retrieve_from_query(query, top_k=2):
    # retrieve from Pinecone
    embedded_question = openai.Embedding.create(
        input=[query], engine=embed_model)['data'][0]['embedding']

    # get relevant contexts (including the questions)
    query_result = index.query(
        embedded_question, top_k=top_k, include_metadata=True)
    return query_result


def retrieve_relevant_text(query_result):
    # get relevant contexts (including the questions)
    texts = [x['metadata']['text'] for x in query_result['matches']]
    context = '\n\n'.join(texts)
    return context


def get_source_info(query_result):
    info = ""
    for x in query_result['matches']:
        document = x['metadata']['document']
        page_num = x['metadata']['page_num']
        info += "Document: " + document + ",  Page #: " + str(page_num) + "\n"

    return info

# print(get_source_info(query_result))

# %%


# %%
query = "How do I change my oil?"

query_result = retrieve_from_query(query, top_k=2)
text = retrieve_relevant_text(query_result)
source_info = get_source_info(query_result)
# print(query_result)

print(text)
print(source_info)


# %%
system_prompt_template = """You are a expert mechanic. You are helping a customer with a car repair problem.\
You answer the customer's question and provide a snippet to a relevant page in the repair manual.\
The relevant page of the specific repair manual is provided below.\n \
Repair manual:\n {context} \n\n
proceed to answer the customer's question.\n\n"""


def answer_question(question, system_prompt_template, retrieved_text):

    system_prompt = system_prompt_template.format(context=retrieved_text)
    # print(system_prompt)
    # print(question)
    chat_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}])

    answer = chat_response.choices[0].message.content
    return answer


# %%
query = "How do I change my oil?"
query_result = retrieve_from_query(query, top_k=2)
retrieved_text = retrieve_relevant_text(query_result)
answer = answer_question(query, system_prompt_template, retrieved_text)
print(answer)


# %%
