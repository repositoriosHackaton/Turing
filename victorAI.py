# Importando librerias.
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pypdf import PdfReader

fine_tunned = 'ft:gpt-3.5-turbo-0125:personal:watch-assitance:9g22spel:ckpt-step-32'

# Esquema utilizado para el desarrollo del chat.
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

class Chatbot:
    def __init__(self, api_key, data_path):
        # Estableciendo conexion con la api.
        if not load_dotenv(api_key):
            print('No se pudo establecer conexion a la API.')
        # Seleccionando el modelo a utiliza.
        self.__chat = ChatOpenAI(model='gpt-4o')
        # Procesando la data que  sera utilizada para RAG,
        self._source_knowledge = self._doc_processing(data_path)
        self._messages = []
    
    def _doc_processing(self, data_path):
        """
            Realiza el pre procesamiento de la data que sera utilizada para el RAG. Convirtiendola en un solo documento.
            
            Inputs:
                    data_path: Path donde la data esta siendo almacenada.
            
            Returs:
                    (str): Documento transformado a una string.
        """
        file = PdfReader(data_path)
        source_knowledge  = ''

        for i in range(len(file.pages)):
            source_knowledge  += file.pages[i].extract_text()
        
        return source_knowledge
    
    def chat(self, input_):
        """
            
        """
        # Estructura de prompt
        augmented_prompt = f"""Eres un asistente virtual amable y servicial que utiliza datos recopilados por 
            un reloj inteligente para responder a las consultas de los usuarios. Siempre debes proporcionar 
            respuestas precisas y útiles basadas en la información disponible, asegurándote de mantener un tono 
            amigable y comprensivo. Ten en cuenta la privacidad y la seguridad de los datos del usuario en todo momento.
            Cuando recibas una consulta, sigue estos pasos:

            1. **Saludo y confirmación de comprensión:**
               - Saluda al usuario de manera cordial.
               - Asegúrate de comprender completamente la consulta del usuario.

            2. **Análisis de datos:**
               - Accede a los datos relevantes del reloj inteligente del usuario (como ritmo cardíaco, pasos, sueño, 
                 actividad física, etc.).
               - Analiza la información para proporcionar una respuesta informada.

            3. **Respuesta personalizada:**
               - Proporciona una respuesta precisa y personalizada basada en los datos analizados.
               - Ofrece consejos o sugerencias útiles si es pertinente.
               - Usa un tono amigable y empático en todo momento.

            4. **Despedida y ofrecimiento de ayuda adicional:**
               - Pregunta al usuario si necesita más ayuda.
               - Despídete cordialmente y anima al usuario a volver si tiene más preguntas.

            Contexto:
            {self._source_knowledge}

            Pregunta: {input_}"""
        
        # Enviando el promt al modelo.
        prompt = HumanMessage(content=augmented_prompt)
        
        # Agregando el mensaje al historial
        self._messages.append(prompt)
        
        # Obteniendo la respuesta del modelo.
        response = self.__chat.invoke(self._messages)
        
        # Retornando la respuesta en un formalo interpretable.
        return response.content