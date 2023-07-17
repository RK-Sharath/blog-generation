import streamlit as st
from langchain.prompts import PromptTemplate
from genai.extensions.langchain import LangChainInterface
from genai.schemas import ModelType, GenerateParams
from genai.model import Credentials

st.title("Content generator")
st.caption("This app was developed by Sharath Kumar RK, IBM Ecosystem Engineering Watsonx team")

genai_api_key = st.sidebar.text_input("GenAI API Key", type="password")
genai_api_url = st.sidebar.text_input("GenAI API URL", type="default")
max_tokens = st.sidebar.text_input("Max new tokens", type="default")
min_tokens = st.sidebar.text_input("Min new tokens", type="default")
decoding_method = st.sidebar.text_input("Decoding method (Choose either greedy or sample) ", type="default")
repetition_penalty = st.sidebar.text_input("Repetition penalty (Choose either 1 or 2)" , type="default")
temperature = st.sidebar.text_input("Temperature (Choose a decimal number between 0 & 2)" , type="default")



def blog_outline(topic):
    # Create a creds object
    creds = Credentials(api_key=genai_api_key, api_endpoint=genai_api_url)
    # Define parameters
    params = GenerateParams(decoding_method=decoding_method, temperature=temperature, max_new_tokens=max_tokens, min_new_tokens=min_tokens, repetition_penalty=repetition_penalty)
    # Instantiate LLM model
    llm=LangChainInterface(model=ModelType.FLAN_UL2, params=params, credentials=creds)
    # Prompt
    template = "As an experienced professional, write about {topic}."
    prompt = PromptTemplate(input_variables=["topic"], template=template)
    prompt_query = prompt.format(topic=topic)
    # Run LLM model
    response = llm(prompt_query)
    # Print results
    return st.info(response)


with st.form("myform"):
    topic_text = st.text_input("Enter prompt:", "")
    submitted = st.form_submit_button("Submit")
    if submitted and genai_api_key.startswith('pak-'):
        with st.spinner('Working on it...'):
            if not genai_api_key:
                st.info("Please add your GenAI API KEY & GenAI API URL to continue.")
            elif submitted:
                blog_outline(topic_text)
