import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    
    #Primero: Listar todos los vuelos.
    flights = db.execute("SELECT id, origin, destination, duration FROM flights").fetchall()
    for flight in flights:
        print(f"Flights {flight.id}: {flight.origin} to {flight.destination}, {flight.duration} minutes.")
     
    #segundo: Solicitar al usuario que elija un vuelo.
    flight_id = int(input("\nFlight ID: "))
    flight = db.execute("SELECT origin, destination, duration FROM flights WHERE id = :id",{"id": flight_id}).fetchone() 

    #Asegurarse de que el nuevo vuela sea válido.
    if flight is None:
        print("Error: No existe tal vuelo.")
        return
    
    #Tercero: Lista de pasajeros.
    passengers = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",{"flight_id": flight_id}).fetchall()
    
    print("\nPasajeros:")
    for passenger in passengers:
        print(passenger.name)
    
    if len(passengers) == 0:
        print("No hay pasajeros")
if __name__ == "__main__":
    main()