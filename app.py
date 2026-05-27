import threading
import bot_registro
from flask import Flask, render_template, request, redirect
import json
import requests

app = Flask(__name__)

import os

TOKEN = os.environ.get("TOKEN")

# -------------------------
# CARGAR AGUA
# -------------------------
def cargar_agua():

    with open("agua.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

# -------------------------
# GUARDAR AGUA
# -------------------------
def guardar_agua(datos):

    with open("agua.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

# -------------------------
# CARGAR VECINOS
# -------------------------
def cargar_vecinos():

    with open("vecinos.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

# -------------------------
# ENVIAR MENSAJES
# -------------------------
def enviar_notificaciones(mensaje):

    vecinos = cargar_vecinos()

    for vecino in vecinos:

        chat_id = vecino["chat_id"]

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

        datos = {
            "chat_id": chat_id,
            "text": mensaje
        }

        try:
            requests.post(url, data=datos)

        except:
            print("Error enviando mensaje")

# -------------------------
# PAGINA PRINCIPAL
# -------------------------
@app.route("/")
def inicio():

    agua = cargar_agua()

    return render_template("index.html", agua=agua)

# -------------------------
# ACTUALIZAR AGUA
# -------------------------
@app.route("/actualizar", methods=["POST"])
def actualizar():

    hay_agua = request.form["hay_agua"] == "true"

    cantidad = request.form["cantidad"]

    # Agregar %
    if "%" not in cantidad:
        cantidad += "%"

    hora_llegada = request.form["hora_llegada"]

    mensaje = request.form["mensaje"]

    nuevos_datos = {
        "hay_agua": hay_agua,
        "cantidad": cantidad,
        "hora_llegada": hora_llegada,
        "mensaje": mensaje
    }

    guardar_agua(nuevos_datos)

    texto = f"""
🚰 ACTUALIZACIÓN DEL AGUA

✅ Hay agua: {hay_agua}

💧 Cantidad: {cantidad}

⏰ Hora:
{hora_llegada}

📢 Mensaje:
{mensaje}
"""

    enviar_notificaciones(texto)

    return redirect("/")

# -------------------------
# EJECUTAR
# -------------------------
if __name__ == "__main__":

    # Ejecutar bot en segundo plano
    hilo_bot = threading.Thread(
        target=bot_registro.iniciar_bot
    )

    hilo_bot.start()

    # Ejecutar Flask
    app.run(
        host="0.0.0.0",
        port=10000
    )


