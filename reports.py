from sqlalchemy import text
from database import SessionLocal
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def create_aggregate_view():
    session = SessionLocal()
    try:
        session.execute(text("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS flight_aggregates AS
            SELECT
                DATE_TRUNC('hour', f.departure_time) AS period,
                'hour' AS period_type,
                a.model AS aircraft_model,
                a.airline AS airline_name,
                COUNT(*) AS flights_count
            FROM flights f
            JOIN aircrafts a ON f.aircraft_id = a.id
            WHERE 
                f.area = 'Black Sea'
                AND f.departure_time > '1970-01-01'
            GROUP BY period, aircraft_model, airline_name
            
            UNION ALL
            
            SELECT
                DATE_TRUNC('day', f.departure_time) AS period,
                'day' AS period_type,
                a.model AS aircraft_model,
                a.airline AS airline_name,
                COUNT(*) AS flights_count
            FROM flights f
            JOIN aircrafts a ON f.aircraft_id = a.id
            WHERE
                f.area = 'Black Sea' 
                AND f.departure_time > '1970-01-01'
            GROUP BY period, aircraft_model, airline_name"""))
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

def get_aggregated_report(period_type='day'):
    session = SessionLocal()
    try:
        result = session.execute(text("""
                SELECT period, aircraft_model, airline_name, flights_count
                FROM flight_aggregates
                WHERE period_type = :period_type
                ORDER BY period DESC, flights_count DESC
            """), {'period_type': period_type})

        return [{
            'period': row[0].strftime("%Y-%m-%d %H:%M"),
            'model': row[1],
            'airline': row[2],
            'count': row[3]
        } for row in result]
    finally:
        session.close()

def generate_pdf_file(data, filename):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    headers = ["Period", "Model", "Airline", "Flight Count"]
    table_data = [headers]
    for item in data:
        table_data.append([
            item['period'],
            item['model'],
            item['airline'],
            str(item['count'])
        ])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    doc.build(elements)

