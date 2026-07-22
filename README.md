# Agente Corporativo ITSVA 🎓🤖

Proyecto desarrollado para el Challenge Alura Agente (Inmersión de IA).

Este proyecto implementa un asistente virtual basado en Inteligencia Artificial diseñado para consultar y resolver dudas sobre el Reglamento Estudiantil del Instituto Tecnológico Superior de Valladolid (ITSVA). Utiliza una arquitectura RAG (Retrieval-Augmented Generation) para buscar información en documentos oficiales y generar respuestas precisas.

## Características principales
* **Arquitectura RAG:** Extrae información precisa de reportes y reglamentos internos en formato PDF.
* **Base de Datos Vectorial:** Emplea Chroma DB para el almacenamiento y búsqueda eficiente de los embeddings.
* **Modelo LLM:** Configurado para trabajar con el modelo Google Gemini (Gemini 1.5 Flash).
* **Interfaz de chat:** Incluye una aplicación web para el usuario final construida con Streamlit.

## Tecnologías utilizadas
* **Lenguaje:** Python
* **Frameworks:** LangChain, Streamlit
* **LLM & Embeddings:** Google Generative AI (`langchain-google-genai`)
* **Vector Store:** Chroma
* **Utilidades:** `python-dotenv`, `pypdf`
* **Despliegue:** Oracle Cloud Infrastructure (OCI) - Instancia Ubuntu Ampere

## Requisitos previos
Necesitarás tu propia API Key de Google configurada en un archivo `.env` en la raíz del proyecto:
`GOOGLE_API_KEY="tu_api_key_aqui"`

## Instalación y Uso

1. Clonar el repositorio y crear un entorno virtual.
2. Instalar las dependencias:
   ```bash
   pip install langchain-community langchain-google-genai streamlit chromadb pypdf python-dotenv
Ejecutar la aplicación:
streamlit run app.py

## Ejemplos de preguntas y respuestas
Ejemplo 1 (Pregunta válida)

Pregunta: ¿Cuál es la calificación mínima aprobatoria para las asignaturas y qué pasa si no la alcanzo?

Respuesta del Agente: Los fragmentos no especifican el valor numérico, sin embargo, el reglamento establece lo siguiente: Si aprueba como mínimo el 40% de las unidades, tendrá derecho a evaluación de segunda oportunidad (Artículo 56 y 58). Si no logra aprobar el 40%, la asignatura se asentará como no acreditada (NA) y tendrá derecho a repetir (Artículo 56 y 57).

Ejemplo 2 (Pregunta fuera de contexto / Seguridad)

Pregunta: ¿Cuáles son los precios del menú de la cafetería y a qué hora abren?

Respuesta del Agente: Lo siento, no encuentro esa información en el reglamento vigente del ITSVA. Si tienes alguna otra duda relacionada con las normas académicas, estaré encantado de ayudarte.
## Evidencia del Deploy en OCI (Oracle Cloud)
El agente fue desplegado exitosamente en una instancia de Oracle Cloud Infrastructure. A continuación, la evidencia de la ejecución remota y el funcionamiento:
<img width="2560" height="1599" alt="Screenshot 2026-07-21 190959" src="https://github.com/user-attachments/assets/b412e80d-41e5-4b0e-80a6-2947b214ff81" />
<img width="2558" height="1445" alt="Screenshot 2026-07-21 185646" src="https://github.com/user-attachments/assets/0749c128-4e84-4256-adfb-e6ace27c6be6" />
<img width="2560" height="1599" alt="Screenshot 2026-07-21 185740" src="https://github.com/user-attachments/assets/82b6a4fc-8d26-4064-b32a-9591de839e03" />
<img width="2560" height="1599" alt="Screenshot 2026-07-21 185816" src="https://github.com/user-attachments/assets/897a0f7c-eac5-46af-9b03-60889662ffac" />

