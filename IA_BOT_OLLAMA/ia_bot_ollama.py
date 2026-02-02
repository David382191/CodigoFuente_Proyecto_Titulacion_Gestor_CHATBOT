from flask import Flask, render_template, Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import os
from database.db import get_db
import openai
from models import obtener_conversacion, guardar_mensaje, buscar_palabra_clave
#############################################################################
# Blueprint
bot_bp = Blueprint("bot_bp", __name__)
#############################################################################
# Leer la API Key desde variables de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")
#############################################################################
# Función para responder usando OpenAI
def responder_ia(texto):
    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content": texto}]
    )
    return respuesta.choices[0].message.content
#############################################################################
# Endpoint de WhatsApp
@bot_bp.route("/bot", methods=["POST"])
def whatsapp_bot():
    mensaje_usuario = request.form.get("Body", "").strip()

    # Obtener o crear conversación
    id_conv = obtener_conversacion()
    guardar_mensaje(id_conv, "usuario", mensaje_usuario)

    # Revisar palabra clave
    respuesta = buscar_palabra_clave(mensaje_usuario)

    # Si no hay palabra clave → IA
    if not respuesta:
        respuesta = responder_ia(mensaje_usuario)

    guardar_mensaje(id_conv, "bot", respuesta)

    # Responder a Twilio
    resp = MessagingResponse()
    resp.message(respuesta)

    return str(resp)
#############################################################################
def buscar_palabra_clave(texto_usuario):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT Respuesta_designada 
        FROM PALABRA_CLAVE 
        WHERE %s LIKE CONCAT('%', Palabra, '%');
    """

    cursor.execute(query, (texto_usuario,))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        return resultado["Respuesta_designada"]
    
    return None
#############################################################################
def guardar_mensaje(id_conversacion, remitente, contenido):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO MENSAJE (ID_CONVERSACION, Remitente, Contenido, Fecha_hora)
        VALUES (%s, %s, %s, %s)
    """, (id_conversacion, remitente, contenido, datetime.now()))

    conn.commit()
    cursor.close()
    conn.close()
#############################################################################