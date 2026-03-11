# 🍦 Chatbot WhatsApp para Heladería — Guía completa

## ¿Qué hay en esta carpeta?

| Archivo | Para qué sirve |
|---|---|
| `main.py` | El código del servidor (el cerebro) |
| `requirements.txt` | Las librerías que necesita Python |
| `.env.example` | Plantilla para tus claves secretas |
| `Procfile` | Le dice a Railway cómo arrancar el servidor |

---

## PASO 1 — Conseguir la clave de Claude

1. Entrá a https://console.anthropic.com
2. Creá una cuenta (es gratis para empezar)
3. Andá a **API Keys → Create Key**
4. Copiá la clave (empieza con `sk-ant-...`)
5. Guardala en un bloc de notas

---

## PASO 2 — Conseguir las claves de Twilio

1. Entrá a https://twilio.com → Sign up gratis
2. Una vez adentro, en el dashboard principal vas a ver:
   - **Account SID** (empieza con `AC...`)
   - **Auth Token** (hacé click en "show")
3. Guardá ambos en tu bloc de notas
4. Andá a **Messaging → Try it out → Send a WhatsApp message**
5. Seguí los pasos para activar el sandbox de WhatsApp

---

## PASO 3 — Subir el código a GitHub

1. Entrá a https://github.com y creá una cuenta gratis
2. Creá un **New Repository** (llamalo `chatbot-heladeria`)
3. Subí los 4 archivos de esta carpeta (**NO subas el .env con tus claves reales**)

---

## PASO 4 — Deployar en Railway

1. Entrá a https://railway.app → Login con GitHub
2. **New Project → Deploy from GitHub repo**
3. Seleccioná tu repositorio `chatbot-heladeria`
4. Railway va a detectar automáticamente que es Python
5. Andá a **Variables** y agregá una por una:
   - `ANTHROPIC_API_KEY` = tu clave de Claude
   - `TWILIO_ACCOUNT_SID` = tu SID de Twilio
   - `TWILIO_AUTH_TOKEN` = tu token de Twilio
6. Hacé click en **Deploy**
7. Railway te va a dar una URL como: `https://chatbot-heladeria.up.railway.app`

---

## PASO 5 — Conectar Twilio con tu servidor

1. En Twilio, andá a **Messaging → Settings → WhatsApp Sandbox Settings**
2. En el campo **"When a message comes in"**, pegá:
   ```
   https://TU-URL-DE-RAILWAY.up.railway.app/webhook
   ```
3. Asegurate de que el método sea **HTTP POST**
4. Guardá los cambios

---

## PASO 6 — ¡Probar!

1. Mandá un mensaje al número de sandbox de Twilio desde tu WhatsApp
2. El bot debería responder en segundos 🎉

---

## Personalizar para cada heladería cliente

En el archivo `main.py`, buscá la sección marcada con:
```
# 🔧 PERSONALIZACIÓN - Editá esto para cada heladería cliente
```

Cambiá:
- `NOMBRE_HELADERIA` — El nombre del local
- `NOMBRE_BOT` — El nombre del asistente
- `SYSTEM_PROMPT` — El menú, precios, horarios y dirección

---

## Costos aproximados (por heladería por mes)

| Servicio | Costo estimado |
|---|---|
| Claude API (~5000 mensajes) | ~$3 USD |
| Twilio (~5000 mensajes) | ~$25 USD |
| Railway (servidor) | Gratis o $5 USD |
| **Total** | **~$30 USD/mes** |

Podés cobrarle a la heladería $50-100 USD/mes y tener buen margen 💰

---

## ¿Problemas?

- El servidor no arranca → Revisá que las variables de entorno estén bien cargadas en Railway
- El bot no responde → Verificá que la URL del webhook en Twilio sea correcta (con `/webhook` al final)
- Respuestas raras → Editá el `SYSTEM_PROMPT` en `main.py` con info correcta del local
