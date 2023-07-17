import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from genai.extensions.langchain import LangChainInterface
from genai.schemas import ModelType, GenerateParams
from genai.model import Credentials

st.title("Blog Generator")
st.caption("This app was developed by Sharath Kumar RK, Ecosystem Engineering Watsonx team")

genai_api_key = st.sidebar.text_input("GenAI API Key", type="password")
genai_api_url = st.sidebar.text_input("GenAI API URL", type="default")
max_tokens = st.sidebar.text_input("Max new tokens", type="default")
min_tokens = st.sidebar.text_input("Min new tokens", type="default")
decoding_method = st.sidebar.text_input("Decoding method", type="default")
st.caption("Choose greedy or sample")
repetition_penalty = st.sidebar.text_input("Repetition penalty", type="default")
st.caption("Choose either 1 or 2")
temperature = st.sidebar.text_input("Temperature", type="default")
st.caption("Choose values between 0 & 2")



def blog_outline(topic):
    # Create a creds object
    creds = Credentials(api_key=genai_api_key, api_endpoint=genai_api_url)
    # Define parameters
    params = GenerateParams(decoding_method=decoding_method, temperature=temperature, max_new_tokens=max_tokens, min_new_tokens=min_tokens, repetition_penalty=repetition_penalty)
    # Instantiate LLM model
    llm=LangChainInterface(model=ModelType.FLAN_T5_11B, params=params, credentials=creds)
    # Prompt
    template = "As an experienced professional, generate an outline for a blog about {topic}."
    prompt = PromptTemplate(input_variables=["topic"], template=template)
    prompt_query = prompt.format(topic=topic)
    # Run LLM model
    response = llm(prompt_query)
    # Print results
    return st.info(response)


with st.form("myform"):
    topic_text = st.text_input("Enter prompt:", "")
    submitted = st.form_submit_button("Submit")
    if not genai_api_key:
        st.info("Please add your GenAI API key to continue.")
    elif submitted:
        blog_outline(topic_text)
