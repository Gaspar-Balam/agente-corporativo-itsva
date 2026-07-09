from langchain_community.document_loaders import PyPDFLoader

# Le indicamos la ruta de uno de tus documentos
ruta_pdf = "docs/Reglamento Estudiantil.pdf"

# Usamos la herramienta de LangChain para cargar el PDF
loader = PyPDFLoader(ruta_pdf)
documentos = loader.load()

# Imprimimos cuántas páginas tiene y el texto de la primera página
print(f"El documento tiene {len(documentos)} páginas.")
print("\n--- Texto de la página 1 ---")
print(documentos[0].page_content)