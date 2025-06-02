import streamlit as st
import random
from agents.agent import Agent
import uuid

agent = Agent()

config_id = uuid.uuid4()

st.title("\*\*FAQ\*\*")

openai_api_key = st.sidebar.text_input("OpenAI API Key = 'sk-'", type="password")


def generate_response(query: str) -> str:
   # model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
    #st.info(model.invoke(input_text))
    #response = random.choice(['Hello', 'Hola', 'Aloha', 'Ciao'])
    response = agent.get_response(query, config_id)['messages'][-1].content
    st.info(response)


with st.form("my_form"):
    text = st.text_area(
        "What can I help you with?",
        "",
    )
    submitted = st.form_submit_button("Submit")
    #if not openai_api_key.startswith("sk-"):
        #st.warning("Please enter your OpenAI API key!", icon="⚠")

    if submitted:
        generate_response(text)