import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
# Cargar la llave de tu archivo .env
load_dotenv()

# 1. Reconectar el "Cerebro Matemático" y abrir la base de datos local
print("1. Conectando a la base de datos...")
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# 2. Configurar el LLM (El modelo de lenguaje que redactará la respuesta final)
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0.3)

# 3. Crear la cadena de Retrieval-Augmented Generation (RAG)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff", 
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}) 
)

# 4. ¡La prueba de fuego!
pregunta = "¿Cuáles son los derechos de los estudiantes según el reglamento?"
print(f"\nPregunta del colaborador: {pregunta}")
print("Generando respuesta...\n")

respuesta = qa_chain.invoke(pregunta)

print("--- RESPUESTA DEL AGENTE ---")
print(respuesta['result'])
print("----------------------------")