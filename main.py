"""
🍦 CHATBOT WHATSAPP - HELADERÍA
================================
Servidor webhook que conecta WhatsApp (Twilio) con Claude AI.

INSTRUCCIONES:
1. Completá las variables en el archivo .env
2. Deployá en Railway (instrucciones en README.md)
3. Pegá la URL del servidor en Twilio como webhook
"""

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ============================================================
# 🔧 PERSONALIZACIÓN - Editá esto para cada heladería cliente
# ============================================================
NOMBRE_HELADERIA = "Heladería El Pingüino"
NOMBRE_BOT = "Pingo"

SYSTEM_PROMPT = f"""Sos el asistente virtual de "{NOMBRE_HELADERIA}". Tu nombre es {NOMBRE_BOT} 🐧.

MENÚ ACTUAL:
🍦 HELADOS ARTESANALES (por kilo: $8.500 | 1/4 kilo: $2.500)
- Dulce de leche granizado
- Dulce de leche con brownie
- Chocolate amargo
- Chocolate blanco con frambuesa
- Crema americana
- Frutilla al agua
- Limón al agua
- Mango maracuyá
- Pistacho (SABOR DEL DÍA ⭐)
- Tiramisú

🥤 OTROS PRODUCTOS
- Licuados de helado: $1.800
- Banana split: $3.200
- Sundae: $2.800
- Copa helada: $2.500

🎂 TORTAS HELADAS
- 1kg: $18.000 | 2kg: $32.000
- Encargos con 48hs de anticipación

HORARIOS: Lunes a viernes 14hs a 22hs | Sábados y domingos 12hs a 23hs
DIRECCIÓN: Av. Corrientes 1234, Buenos Aires
DELIVERY: Solo por Pedidos Ya y Rappi
TELÉFONO: 11-4567-8901

INSTRUCCIONES:
- Respondé siempre en español rioplatense (vos, che, etc.)
- Usá emojis con moderación
- Respuestas cortas y directas (máximo 4 líneas)
- Si alguien quiere pedir, pedile nombre y qué quiere
- Para tortas, recordá que necesitan 48hs de anticipación
- Si no sabés algo, decí que consulten al local por teléfono
"""
# ============================================================

# Memoria de conversaciones por número de teléfono
conversaciones = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    """Recibe mensajes de WhatsApp y responde con Claude."""
    
    # Obtener el mensaje y el número del cliente
    mensaje_cliente = request.form.get("Body", "").strip()
    numero_cliente = request.form.get("From", "")
    
    print(f"📱 Mensaje de {numero_cliente}: {mensaje_cliente}")
    
    # Recuperar historial de conversación (o crear uno nuevo)
    if numero_cliente not in conversaciones:
        conversaciones[numero_cliente] = []
    
    historial = conversaciones[numero_cliente]
    
    # Agregar mensaje del cliente al historial
    historial.append({
        "role": "user",
        "content": mensaje_cliente
    })
    
    # Limitar historial a los últimos 10 mensajes (para no gastar tokens)
    if len(historial) > 10:
        historial = historial[-10:]
        conversaciones[numero_cliente] = historial
    
    # Llamar a Claude
    try:
        respuesta = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            system=SYSTEM_PROMPT,
            messages=historial
        )
        
        texto_respuesta = respuesta.content[0].text
        
    except Exception as e:
        print(f"❌ Error con Claude: {e}")
        texto_respuesta = "¡Ups! Hubo un problemita técnico. Llamanos al 11-4567-8901 🙏"
    
    # Guardar respuesta en el historial
    historial.append({
        "role": "assistant", 
        "content": texto_respuesta
    })
    
    print(f"🤖 Respuesta: {texto_respuesta}")
    
    # Enviar respuesta a WhatsApp via Twilio
    respuesta_twilio = MessagingResponse()
    respuesta_twilio.message(texto_respuesta)
    
    return str(respuesta_twilio)


@app.route("/", methods=["GET"])
def home():
    """Página de inicio para verificar que el servidor está corriendo."""
    return f"""
    <h1>🍦 Chatbot {NOMBRE_HELADERIA}</h1>
    <p>✅ El servidor está funcionando correctamente.</p>
    <p>Webhook URL: <code>/webhook</code></p>
    """


if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    print(f"🚀 Servidor corriendo en puerto {puerto}")
    app.run(host="0.0.0.0", port=puerto, debug=False)
