# Agent_AI_Chatbot

#  Personal Agentic AI Chatbot  
**LangGraph | FastAPI | Streamlit | OpenAI | Groq | Meta LLaMA | Mistral**

A **production-ready GenAI application** built using LangGraph ReAct Agents, FastAPI, and Streamlit.  
This project demonstrates how to set up an end-to-end agentic chatbot system with backend + frontend integration.

---
## 🚀 Live Demo  

![Capture4](https://github.com/user-attachments/assets/9a59c883-5bcd-4641-ba72-7d69b55855da)

## 📂 Project Layout

### Phase 1 – Create AI Agent
1. Setup API Keys (Groq, Tavily, OpenAI)
2. Configure LLM & Tools
3. Setup AI Agent with Search Tool functionality  

### Phase 2 – Backend (FastAPI)
1. Define Pydantic Models for schema validation  
2. Handle AI Agent requests from frontend  
3. Run backend app and explore via **Swagger UI**  

### Phase 3 – Frontend (Streamlit)
1. Build UI with model provider, model selector, system prompt, and query input  
2. Connect with backend using REST API URL  

---

## 🛠️ Tools & Technologies
- **LangGraph ReAct Agents**
- **FastAPI** – Backend API
- **Groq & OpenAI** – LLM providers
- **Streamlit** – Frontend UI
- **LangChain** – Tools & integrations
- **Uvicorn** – ASGI server
- **Python**
- **VS Code**

---

## 🏗️ Technical Architecture

[ User ] → [ Streamlit Frontend ] → [ FastAPI Backend ]
→ [ LangGraph Agent ] → [ Groq / OpenAI / Tools ]
