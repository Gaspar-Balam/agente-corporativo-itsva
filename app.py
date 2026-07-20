import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

# 1. Configuración visual de la página web
st.set_page_config(page_title="Agente ITSVA", page_icon="🎓")
st.title("🎓 Agente Corporativo ITSVA")
st.markdown("Asistente virtual oficial basado en el Reglamento Estudiantil. ¿En qué te puedo ayudar?")

# 2. Cargar el agente en Caché 
# (Para que no vuelva a cargar la base de datos con cada mensaje)
@st.cache_resource
def cargar_agente():
    load_dotenv()
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    
    llm = ChatGoogleGenerativeAI(model="models/gemini-3.5-flash", temperature=0.1)
    
    plantilla = """Eres el Asistente Virtual Oficial del Instituto Tecnológico Superior de Valladolid (ITSVA).
    Tu objetivo es responder dudas de los estudiantes basándote ÚNICAMENTE en los fragmentos del reglamento que se te proporcionan.
    - Si la respuesta no está en el contexto proporcionado, di amablemente: "Lo siento, no encuentro esa información en el reglamento vigente del ITSVA."
    - NUNCA inventes información.
    - Responde de forma cordial, formal y estructurada.

    Fragmentos del reglamento:
    {context}

    Pregunta del estudiante: {question}

    Respuesta oficial:"""
    
    prompt_personalizado = PromptTemplate(
        template=plantilla, input_variables=["context", "question"]
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff", 
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": prompt_personalizado}
    )
    return qa_chain

qa_chain = cargar_agente()

# 3. Memoria del chat en la interfaz web
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Dibujar los mensajes anteriores en la pantalla
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# 4. Caja de texto para que el estudiante escriba
pregunta = st.chat_input("Escribe tu duda sobre el reglamento...")

if pregunta:
    # Mostrar la pregunta del usuario en el chat
    with st.chat_message("user"):
        st.markdown(pregunta)
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    
    # Mostrar mensaje de "pensando..." mientras Gemini trabaja
    with st.chat_message("assistant"):
        with st.spinner("Consultando el reglamento del ITSVA..."):
            respuesta = qa_chain.invoke(pregunta)
            texto_respuesta = respuesta['result']
            st.markdown(texto_respuesta)
    
    # Guardar la respuesta en la memoria
    st.session_state.mensajes.append({"role": "assistant", "content": texto_respuesta})