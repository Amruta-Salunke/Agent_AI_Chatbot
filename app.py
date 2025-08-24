

#Step1: Setup API Keys for Groq, OpenAI and Tavily

import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")


#Step2: Setup LLM & Tools
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

openai_llm =ChatOpenAI(model="gpt-4o-mini")
groq_llm =ChatGroq(model="llama-3.3-70b-versatile")

search_tool=TavilySearchResults(max_results=2)


#Step3: Setup AI Agent with Search tool functionality
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage



def get_response_from_ai_agent(llm_id, query, allow_search, provider):
    if provider=="Groq":
        llm=ChatGroq(model=llm_id)
    elif provider=="OpenAI":
        llm=ChatOpenAI(model=llm_id)

    tools=[TavilySearchResults(max_results=2)] if allow_search else []
    agent=create_react_agent(
        model=llm,
        tools=tools,

    
    )
    state={"messages": query}
    response=agent.invoke(state)
    messages=response.get("messages")
    ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1]


#Step1: Setup Pydantic Model (Schema Validation)

from pydantic import BaseModel
from typing import List


class RequestState(BaseModel):
    model_name: str
    model_provider: str
    messages: List[str]
    allow_search: bool

#Step2: Setup AI Agent from FrontEnd Request
from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent

ALLOWED_MODEL_NAMES=["llama3-70b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile", "gpt-4o-mini"]

app=FastAPI(title="LangGraph AI Agent")

@app.post("/chat")
def chat_endpoint(request:RequestState):
    """
    API Endpoint to interact with the Chatbot using LangGraph and search tools.
    It dynamically selects the model specified in the request
    """
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Invalid model name. Kindly select a valid AI model"}
    
    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    provider = request.model_provider

    # Create AI Agent and get response from it! 
    response=get_response_from_ai_agent(llm_id, query, allow_search, provider)
    return response


#Step3: Run app & Explore Swagger UI Docs
if __name__ =="__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)



#Step1: Setup UI with streamlit (model provider, model, web_search, query)
import streamlit as st

st.set_page_config(page_title="LangGraph Agent UI", layout="centered")


st.markdown(
    """
    <style>
    .block-container {
        max-width: 700px;   /* Adjust width (smaller = narrower page) */
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.title("AI Chatbot Agents")
st.write("Create and Interact with the AI Agents!")

system_prompt=st.text_area("Define your AI Agent: ", height=70, placeholder="Type your system prompt here...")



MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

provider=st.radio("Select Provider:", ("Groq", "OpenAI"))

if provider == "Groq":
    selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)
elif provider == "OpenAI":
    selected_model = st.selectbox("Select OpenAI Model:", MODEL_NAMES_OPENAI)


allow_web_search=st.checkbox("Allow Web Search")

user_query=st.text_area("Enter your query: ", height=150, placeholder="Ask Anything!")

API_URL="http://127.0.0.1:9999/chat"

if st.button("Ask Agent!"):

    
    if user_query.strip(): 

        #Step2: Connect with backend via URL
        import requests

        payload={
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        response=requests.post(API_URL, json=payload)

        #get response from backend and show here

        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.subheader("Agent Response")
                st.markdown(f"**Final Response:** {response_data}")

        # response = "Hi,this is a fixed dummy response"
        # st.subheader("Agent Response")
        # st.markdown(f"**Final Response:** {response}")

   