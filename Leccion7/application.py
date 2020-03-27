import os
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("index.html", flights=flights)


@app.route("/book", methods=["POST"])
def book():
    # Reservar vuelo
    # Obtenemos el nombre de quien reserva.
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Número de vuelo inválido.")
    # Aseguramos que el vuelo exista.
    # Si el número de tuplas que devuelve la consulta es 0
    if db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).rowcount == 0:
        return render_template("error.html", message="No hay tal vuelo con ese id.")
    # De lo contrario
    # Insertar pasajero en la tabla pasajeros según ID seleccionado
    db.execute("INSERT INTO passengers (name, flight_id) VALUES (:name, :flight_id)", {"name": name, "flight_id": flight_id})
    db.commit()
    return render_template("success.html")


