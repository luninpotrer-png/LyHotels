from email.policy import default

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    hotel = db.relationship("Hotel", backref="dueno")
    resena_user = db.relationship("Resenas", backref="usuario")
    reserva_user = db.relationship("Reserva", backref="usuario_reserva")

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.String(20), nullable=False)
    imagen_url = db.Column(db.String(500))
    estado = db.Column(db.String(20), default="pendiente")
    descripcion = db.Column(db.Text, nullable=False)
    ubicacion = db.Column(db.String, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    estrellas = db.Column(db.Integer, default=0)
    numero_contacto = db.Column(db.String(20), nullable=False)
    resena_hotel = db.relationship("Resenas", backref="hotel")
    reserva_hotel = db.relationship("Reserva", backref="hotel_reserva")

class Resenas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    estrellas =db.Column(db.Integer, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    hotel_id = db.Column(db.Integer, db.ForeignKey("hotel.id"))

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_entrada = db.Column(db.String(20), nullable=False)
    fecha_salida = db.Column(db.String(20), nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey("hotel.id"))
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
