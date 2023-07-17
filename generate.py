import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from genai.extensions.langchain import LangChainInterface
from genai.schemas import ModelType, GenerateParams
from genai.model import Credentials

st.title("Blog Generator App")
st.caption("This app was developed by Sharath Kumar RK, Ecosystem Engineering Watsonx team")

genai_api_key = st.sidebar.text_input("GenAI API Key", type="password")
genai_api_url = st.sidebar.text_input("GenAI API URL", type="default")


def blog_outline(topic):
    # Create creds object
    creds = Credentials(api_key=genai_api_key, api_endpoint=genai_api_url)
    # Define parameters
    params = GenerateParams(decoding_method="sample", temperature=0.7, max_new_tokens=400, min_new_tokens=150, repetition_penalty=2)
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
