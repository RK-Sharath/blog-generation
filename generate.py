import streamlit as st
from langchain.prompts import PromptTemplate
from genai.extensions.langchain import LangChainInterface
from genai.schemas import GenerateParams
from genai.model import Credentials

st.title("Content generator App powered by IBM Watsonx")
st.caption("This app was developed by Sharath Kumar RK, IBM Ecosystem Engineering Watsonx team")

genai_api_key = st.sidebar.text_input("GenAI API Key", type="password")
genai_api_url = st.sidebar.text_input("GenAI API URL", type="default")
model = st.radio("Select the Watsonx LLM model",('google/flan-t5-xl','google/flan-t5-xxl','google/flan-ul2'))
max_tokens = st.sidebar.number_input("Max new tokens", value=500)
min_tokens = st.sidebar.number_input("Min new tokens", value=150)
#decoding_method = st.sidebar.text_input("Decoding method (Choose either greedy or sample) ", type="default")
with st.sidebar:
    decoding_method = st.radio(
        "Select decoding method",
        ('sample', 'greedy')
    )
repetition_penalty = st.sidebar.number_input("Repetition penalty (Choose either 1 or 2)", value=2)
temperature = st.sidebar.number_input("Temperature (Choose a decimal number between 0 & 2)", value=0.4)




def gen_content(query):
    # Create a creds object
    creds = Credentials(api_key=genai_api_key, api_endpoint=genai_api_url)
    # Define parameters
    params = GenerateParams(decoding_method=decoding_method, temperature=temperature, max_new_tokens=max_tokens, min_new_tokens=min_tokens, repetition_penalty=repetition_penalty)
    # Instantiate LLM model
    llm=LangChainInterface(model=model, params=params, credentials=creds)
    # Prompt
    template = "As an experienced professional, write about {topic}."
    prompt = PromptTemplate(input_variables=["topic"], template=template)
    prompt_query = prompt.format(topic=query)
    # Run LLM model
    response = llm(prompt_query)
    # Print results
    return st.info(response)


#with st.form("myform"):
query = st.text_input("Enter prompt:", "", placeholder="Ask me a query")
if query and genai_api_key.startswith('pak-'):
    with st.spinner('Working on it...'):
        if not genai_api_key:
            st.info("Please add your GenAI API KEY & GenAI API URL to continue.")
        elif submitted:
            gen_content(query)
