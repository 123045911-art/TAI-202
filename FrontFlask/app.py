from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

API = "http://127.0.0.1:5000/v1/usuarios/"

# Página principal
@app.route("/")
def index():
    response = requests.get(API)
    data = response.json()
    usuarios = data.get("usuarios", [])
    return render_template("index.html", usuarios=usuarios)

# Crear usuario
@app.route("/crear", methods=["POST"])
def crear_usuario():
    nuevo_usuario = {
        "id": int(request.form["id"]),
        "nombre": request.form["nombre"],
        "edad": int(request.form["edad"])
    }
    
    requests.post(API, json=nuevo_usuario)
    return redirect("/")

# Eliminar usuario
@app.route("/eliminar/<int:id>")
def eliminar_usuario(id):
    requests.delete(API + str(id))
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5010)