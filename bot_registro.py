from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

import json

import os
TOKEN = os.environ.get("TOKEN")


# -------------------------
# CARGAR VECINOS
# -------------------------
def cargar_vecinos():

    with open("vecinos.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

# -------------------------
# GUARDAR VECINOS
# -------------------------
def guardar_vecinos(vecinos):

    with open("vecinos.json", "w", encoding="utf-8") as archivo:
        json.dump(vecinos, archivo, indent=4, ensure_ascii=False)

# -------------------------
# CARGAR AGUA
# -------------------------
def cargar_agua():

    with open("agua.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

# -------------------------
# /start
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    nombre = update.effective_user.first_name

    vecinos = cargar_vecinos()

    usuario_existe = False

    for vecino in vecinos:

        if vecino["chat_id"] == chat_id:
            usuario_existe = True
            break

    # Registrar automáticamente
    if not usuario_existe:

        vecinos.append({
            "chat_id": chat_id,
            "nombre": nombre
        })

        guardar_vecinos(vecinos)

    mensaje = f"""
Hola {nombre} 👋

Has sido registrado en el sistema de agua 🚰

Ahora recibirás notificaciones automáticas.
"""

    await update.message.reply_text(mensaje)

# -------------------------
# /estado
# -------------------------
async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE):

    agua = cargar_agua()

    mensaje = f"""
🚰 ESTADO DEL AGUA

✅ Hay agua:
{agua['hay_agua']}

💧 Cantidad:
{agua['cantidad']}

⏰ Hora:
{agua['hora_llegada']}

📢 Mensaje:
{agua['mensaje']}
"""

    await update.message.reply_text(mensaje)

# -------------------------
# CREAR BOT
# -------------------------
app = ApplicationBuilder().token(TOKEN).build()

# -------------------------
# COMANDOS
# -------------------------
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("estado", estado))

# -------------------------
# EJECUTAR BOT
# -------------------------
print("Bot funcionando...")

def iniciar_bot():

    print("Bot funcionando...")

    app.run_polling()


