import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Cargar la llave
load_dotenv()

# 2. Cargar y dividir
print("1. Cargando y dividiendo el documento...")
ruta_pdf = "docs/Reglamento Estudiantil.pdf"
loader = PyPDFLoader(ruta_pdf)
documentos = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
fragmentos = text_splitter.split_documents(documentos)

# 3. Configurar Embeddings
print("2. Conectando con Google Gemini...")
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# 4. Crear Base de Datos con pausas y reintentos (para micro-desconexiones)
print("3. Creando la base de datos local (ChromaDB) en lotes...")
directorio_bd = "./chroma_db"

vectorstore = Chroma(embedding_function=embeddings, persist_directory=directorio_bd)

tamaño_lote = 20
for i in range(0, len(fragmentos), tamaño_lote):
    lote = fragmentos[i : i + tamaño_lote]
    intentos = 0
    exito = False
    
    while intentos < 3 and not exito:
        try:
            print(f"   -> Procesando fragmentos del {i+1} al {min(i+tamaño_lote, len(fragmentos))}...")
            vectorstore.add_documents(lote)
            exito = True
        except Exception as e:
            intentos += 1
            print(f"      [!] Error de red. Reintentando ({intentos}/3) en 5 segundos...")
            time.sleep(5)
            
    if not exito:
        print("      [X] Falló tras 3 intentos. Por favor, verifica tu conexión a internet.")
        break
    
    # Pausa habitual para no saturar la API
    if i + tamaño_lote < len(fragmentos):
        time.sleep(5) 

if exito:
    print(f"\n¡Éxito! Base de datos creada y guardada en la carpeta: {directorio_bd}")