import os

from flask import Flask, request, redirect, session, render_template
from flask.cli import load_dotenv

from models import db, Usuario,Resenas,Reserva,Hotel
from hasheo import hasheo
from datetime import datetime
import cloudinary
import cloudinary.uploader

app = Flask(__name__)
app.secret_key = "MV4T7&M93yxnW4CynPHYkr"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hoteles.db"
db.init_app(app)

#cloudinary usos
load_dotenv()

cloudinary.config(
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure = True
)

with app.app_context():
    db.create_all()

#logica de seguridad en img
EXTENCIONES_PERMITIDAS=["png","jpg","webp","jpeg","gif"]
def es_imagen_valida(nombre_archivo):
    if "." not in nombre_archivo:
        return False
    # rsplit devuelve una lista, comparamos el último elemento
    extension = nombre_archivo.rsplit(".", 1)[1].lower()
    return extension in EXTENCIONES_PERMITIDAS
#fin de logica de seguridad de img

@app.route("/")
def inicio():
    hotels = Hotel.query.filter_by(estado="aprobado").all()
    return render_template("index.html", hotels=hotels)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        usuario = Usuario.query.filter_by(username=request.form["username"]).first()
        if usuario and usuario.password == hasheo(request.form["password"]):
            session["usuario"] = usuario.id
            return redirect("/")
        return render_template("login.html", error="Credenciales Incorrectas")
    return render_template("login.html", error=None)

@app.route("/registro", methods=["GET","POST"])
def registro():
    if request.method == "POST":
        if Usuario.query.filter_by(username=request.form["username_register"]).first():
            return render_template("register.html",error="Este username ya existe")
        if request.form["password_register"] == request.form["password_confirm"]:
            nombre = request.form["nombre"]
            username = request.form["username_register"].strip()
            password = hasheo(request.form["password_register"])
            nuevo_usuario = Usuario(
                nombre=nombre,
                username=username,
                password=password
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            return redirect("/login")
        return render_template("register.html",error="Revisar sus datos")
    return render_template("register.html",error=None)

@app.route("/crear", methods=["GET","POST"])
def crear():
    if "usuario" not in session:
        return redirect("/login")
    if request.method == "POST":
        archivo=request.files.get('imagen')
        url_final= "https://via.placeholder.com/300"
        if archivo and archivo.filename != "":
            if es_imagen_valida(archivo.filename):
                resultado = cloudinary.uploader.upload(archivo)
                url_final=resultado["secure_url"]
    if request.method == "POST":
        autor = Usuario.query.filter_by(id=session["usuario"]).first()
        dueno = Hotel(
            nombre = request.form["nombre_hotel"].strip(),
            fecha = datetime.now().strftime("%d/%m/%Y"),
            descripcion = request.form["descripcion"],
            numero_contacto = request.form["telefono"],
            ubicacion = request.form["ubicacion"],
            estrellas = request.form["estrellas"],
            imagen_url = url_final,
            usuario_id = autor.id
        )
        db.session.add(dueno)
        db.session.commit()
        return redirect("/")
    return render_template("crear.html", error=None)

@app.route("/hotel/<int:id>")
def ver_hotel(id):
    hotel = Hotel.query.get_or_404(id)
    return render_template("hotels.html", hotel=hotel)

@app.route("/comentar/<int:hotel_id>", methods=["POST"])
def comentar(hotel_id):
    if "usuario" not in session:
        return redirect("/login")
    comentario_hotel = Resenas(
        texto = request.form.get("comentario"),
        estrellas = int(request.form.get("estrellas")),
        usuario_id = session["usuario"],
        hotel_id = hotel_id
    )
    db.session.add(comentario_hotel)
    db.session.commit()
    return redirect(f"/hotel/{hotel_id}")

@app.route("/mi_hotel")
def mi_hotel():
    if "usuario" not in session:
        return redirect("/login")
    hotel = Hotel.query.filter_by(usuario_id=session["usuario"]).first()
    return render_template("mi_hotel.html", hotel=hotel)

@app.route("/eliminar/<int:eliminar_id>")
def eliminar_hotel(eliminar_id):
    if "usuario" not in session:
        return redirect("/") 
    hotel=Hotel.query.get_or_404(eliminar_id)
    if hotel.dueno.id != session["usuario"]
        return redirect("/")
    
    db.session.delete(hotel)
    db.session.commit()
    return redirect("/mi_hotel")

@app.route("/admin/panel")
def panel_admin():
    if "usuario" not in session:
        return redirect("/login")
    usuario_actual=Usuario.query.filter_by(id=session["usuario"]).first()
    if usuario_actual.username != "owenacr":
        return render_template("login.html", error="Acceso Denegado: NO TIENES PERMISO DE ADMINISTRADOR")
    pendientes = Hotel.query.filter_by(estado="pendiente").all()
    return render_template("admin.html", hoteles_pendientes=pendientes)

@app.route("/admin/aprobar/<int:id>")
def aprobar_hoteles(id):
    if "usuario" not in session:
        return redirect("/")
    usuario_actual=Usuario.query.filter_by(id=session["usuario"]).first()

    if usuario_actual.username != "owenacr":
        return redirect("/")

    hotel_identificador = Hotel.query.get_or_404(id)
    hotel_identificador.estado = "aprobado"

    db.session.commit()
    return redirect("/admin/panel")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False)
