from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship



Base = declarative_base()

class Aircraft(Base):
    __tablename__ = 'aircrafts'

    id = Column(Integer, primary_key=True)
    callsign = Column(String(255), unique=True, nullable=False)
    icao = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    airline = Column(String(255), nullable=False)
    flights = relationship('Flight_tracking', back_populates='aircraft')

class Flight_tracking(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    aircraft_id = Column(Integer, ForeignKey('aircrafts.id'), nullable=False)
    departure_icao = Column(String(255), nullable=False)
    arrival_icao = Column(String(255), nullable=False)
    # departure_time = Column(String(255), nullable=False)
    # arrival_time = Column(String(255), nullable=False)
    # estimated_travel_time = Column(String(255), nullable=False)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    estimated_travel_time = Column(Float)
    area = Column(String(50))
    aircraft = relationship('Aircraft', back_populates='flights')

    def __init__(self, aircraft_id, departure_icao, arrival_icao, departure_time, arrival_time, estimated_travel_time, area):
        self.aircraft_id = aircraft_id
        self.departure_icao = departure_icao
        self.arrival_icao = arrival_icao
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.estimated_travel_time = estimated_travel_time
        self.area = area


def get_departure_time(flight):
    time_details = flight.time_details
    scheduled = time_details.get('scheduled', {})

    departure_time = scheduled.get('departure')
    return departure_time

def get_arrival_time(flight):
    time_details = flight.time_details
    scheduled = time_details.get('scheduled', {})
    arrival_time = scheduled.get('arrival')
    return arrival_time

def get_estimated_travel_time(flight):
    d_time = get_departure_time(flight)
    a_time = get_arrival_time(flight)
    if d_time and a_time:
        duration = (a_time - d_time) / 3600
        return format(duration, '.1f')
