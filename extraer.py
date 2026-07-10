from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Cargar el documento
ruta_pdf = "docs/Reglamento Estudiantil.pdf"
loader = PyPDFLoader(ruta_pdf)
documentos = loader.load()

# 2. Configurar el divisor de texto (Text Splitter)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, # chunk_size: El tamaño máximo de cada fragmento (en caracteres).
    chunk_overlap=200, # chunk_overlap: El número de caracteres que se solaparán entre un fragmento y el siguiente.
    length_function=len
)

# 3. Dividir las páginas en fragmentos pequeños
fragmentos = text_splitter.split_documents(documentos)

# 4. Verificar la estructura de los datos generados
print(f"El documento original tenía {len(documentos)} páginas.")
print(f"Tras la segmentación, tenemos {len(fragmentos)} fragmentos (chunks) listos para la IA.")

# Imprimir un fragmento de prueba para validar el contenido y sus metadatos
if len(fragmentos) > 5:
    print("\n--- Ejemplo del Fragmento #5 ---")
    print(fragmentos[4].page_content)
    print("\n--- Metadatos del Fragmento ---")
    print(fragmentos[4].metadata)