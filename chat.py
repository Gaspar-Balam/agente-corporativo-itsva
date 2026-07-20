import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate  # <-- Importamos la herramienta para dar instrucciones

# 1. Cargar configuración y Base de Datos
load_dotenv()
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# 2. Configurar el LLM
llm = ChatGoogleGenerativeAI(model="models/gemini-3.5-flash", temperature=0.1)

# 3. EL INGENIERO DE PROMPTS (Instrucciones estrictas)
plantilla = """Eres el Asistente Virtual Oficial del Instituto Tecnológico Superior de Valladolid (ITSVA).
Tu objetivo es responder dudas de los estudiantes basándote ÚNICAMENTE en los fragmentos del reglamento que se te proporcionan.
- Si la respuesta no está en el contexto proporcionado, di amablemente: "Lo siento, no encuentro esa información en el reglamento vigente del ITSVA."
- NUNCA inventes información.
- Responde de forma cordial, formal y estructurada.

Fragmentos del reglamento:
{context}

Pregunta del estudiante: {question}

Respuesta oficial del ITSVA:"""

# Empaquetamos la plantilla
prompt_personalizado = PromptTemplate(
    template=plantilla, input_variables=["context", "question"]
)

# 4. Crear la cadena RAG con nuestras instrucciones inyectadas
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff", 
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    chain_type_kwargs={"prompt": prompt_personalizado} # <-- Aquí le pasamos las reglas
)

# 5. Interfaz de Validación en Terminal (Loop)
print("\n" + "="*50)
print("🤖 AGENTE CORPORATIVO ITSVA INICIADO")
print("Escribe tu pregunta (o 'salir' para terminar).")
print("="*50 + "\n")

while True:
    pregunta = input("Estudiante: ")
    
    if pregunta.lower() in ['salir', 'exit', 'quit']:
        print("Apagando agente... ¡Hasta luego!")
        break
        
    print("Agente: Buscando en el reglamento...\n")
    respuesta = qa_chain.invoke(pregunta)
    print(f"--- RESPUESTA ---\n{respuesta['result']}\n-----------------\n")