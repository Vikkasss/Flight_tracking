from datetime import datetime
from flightradar24.api import FlightRadar24API
from data_loader import add_aircraft, add_flight
from database import SessionLocal
from models import Aircraft, Flight_tracking, get_departure_time, get_arrival_time, get_estimated_travel_time
from sqlalchemy import text
from reports import create_aggregate_view, generate_pdf_file, get_aggregated_report

#Base.metadata.drop_all(bind=engine)
#Base.metadata.create_all(bind=engine)

fr_api = FlightRadar24API()
# Задаем границы Черного моря
latitude = 43.3  # Широта центра Черного моря
longitude = 34.0  # Долгота центра Черного моря
radius_meters = 650_000  # 650 км

bounds = fr_api.get_bounds_by_point(latitude,longitude, 650_000)

session = SessionLocal()
flights = fr_api.get_flights(bounds=bounds)
flights = flights[0:15]
for flight in flights:
    try:
        flight_details = fr_api.get_flight_details(flight)
        flight.set_flight_details(flight_details)

        departure_t = datetime.fromtimestamp(get_departure_time(flight))
        arrival_t = datetime.fromtimestamp(get_arrival_time(flight))
        estimated_t = get_estimated_travel_time(flight)

        if not all(hasattr(flight, attr) for attr in ['callsign', 'origin_airport_iata', 'destination_airport_iata']):
            continue

        aircraft = session.query(Aircraft).filter_by(callsign=flight.callsign).first()
        if not aircraft:
            aircraft = add_aircraft(
                callsign=flight.callsign,
                icao=getattr(flight, 'airline_icao', flight.origin_airport_iata),
                model=getattr(flight, 'aircraft_code', getattr(flight, 'registration', 'UNKNOWN')),
                airline=getattr(flight, 'airline_iata', None)
            )


        # Проверяем существование такого же рейса
        if not session.query(Flight_tracking).filter_by(
            aircraft_id=aircraft.id,
            departure_icao=flight.origin_airport_iata,
            arrival_icao=flight.destination_airport_iata
        ).first():
            add_flight(
                aircraft_id=aircraft.id,
                departure_icao=flight.origin_airport_iata,
                arrival_icao=flight.destination_airport_iata,
                departure_time=departure_t,
                arrival_time=arrival_t,
                estimated_travel_time=estimated_t,
                area='Black Sea'
            )
    except Exception as e:
        print(f"Skipping flight due to error: {e}")
        continue

print('Данные успешно добавлены в таблицы!')

session.commit()

create_aggregate_view()
try:
    session.execute(text("REFRESH MATERIALIZED VIEW CONCURRENTLY flight_aggregates"))
    session.commit()
except Exception as e:
    print(f"Ошибка обновления витрины: {e}")
    session.rollback()


# Отладочная информация
print("\nОтладочная информация:")
print(f"Самолеты: {session.query(Aircraft).count()}")
print(f"Рейсы: {session.query(Flight_tracking).count()}")

# Генерация отчета
try:
    daily_report = get_aggregated_report('hour')
    print("\nDaily Report:")
    for item in daily_report:
        print(f"{item['period']} | {item['model']} | {item['airline']}: {item['count']} flights")

    generate_pdf_file(daily_report, "flight_report.pdf")
    print('\nОтчет также сохранен в PDF файл')
except Exception as e:
    print(f"Ошибка генерации отчета: {e}")
session.close()
