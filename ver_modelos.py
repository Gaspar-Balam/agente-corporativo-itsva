import os
import requests
from dotenv import load_dotenv

# Cargamos tu llave secreta
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print("Consultando a los servidores de Google...\n")

# Hacemos una petición directa a la API de Google
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
respuesta = requests.get(url)

if respuesta.status_code == 200:
    datos = respuesta.json()
    print("¡Estos son los modelos que tienes autorizados para generar texto!")
    print("-" * 50)
    for modelo in datos.get('models', []):
        # Filtramos solo los que sirven para responder preguntas (generateContent)
        if 'generateContent' in modelo.get('supportedGenerationMethods', []):
            print(f"-> {modelo['name']}")
    print("-" * 50)
else:
    print("Hubo un error al consultar:", respuesta.text)