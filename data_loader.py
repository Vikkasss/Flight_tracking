from models import Aircraft, Flight_tracking
from database import SessionLocal

session = SessionLocal()

def add_aircraft(callsign, icao, model, airline):
    aircraft = Aircraft(
        callsign=callsign,
        icao=icao,
        model=model,
        airline=airline
    )
    session.add(aircraft)
    session.commit()
    return aircraft

def add_flight(aircraft_id, departure_icao, arrival_icao, departure_time, arrival_time, estimated_travel_time, area):
    try:
        flight = Flight_tracking(
            aircraft_id=aircraft_id,
            departure_icao=departure_icao,
            arrival_icao=arrival_icao,
            departure_time=departure_time,
            arrival_time=arrival_time,
            estimated_travel_time=estimated_travel_time,
            area=area
        )
        session.add(flight)
        session.commit()
        return flight
    except Exception as e:
        session.rollback()
        print(f"Error adding flight: {e}")
        raise
