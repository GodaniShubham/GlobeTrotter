import random
import datetime

def get_transport_options(origin, destination, date_str):
    """
    Mock service to simulate real-time APIs like Amadeus or Duffel.
    Generates realistic schedules for Flights, Trains, and Buses based on distance heuristics.
    """
    try:
        travel_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        travel_date = datetime.date.today()

    # Determine if it's a short haul or long haul based on basic heuristics or just random
    # For prototype, we just generate 3 flights, 2 trains, and 2 buses with varying prices and durations.
    
    options = []
    
    # --- FLIGHTS ---
    airlines = ['Air France', 'Lufthansa', 'British Airways', 'Emirates', 'Delta', 'Ryanair', 'easyJet']
    for i in range(random.randint(2, 4)):
        departure_hour = random.randint(6, 20)
        departure_min = random.choice([0, 15, 30, 45])
        dep_time = datetime.datetime.combine(travel_date, datetime.time(departure_hour, departure_min))
        
        duration_hrs = random.uniform(1.5, 4.0)
        duration_delta = datetime.timedelta(hours=duration_hrs)
        arr_time = dep_time + duration_delta
        
        options.append({
            'type': 'Flight',
            'provider': random.choice(airlines),
            'departure_time': dep_time.isoformat(),
            'arrival_time': arr_time.isoformat(),
            'duration': f"{int(duration_hrs)}h {int((duration_hrs % 1)*60)}m",
            'price_usd': round(random.uniform(50, 350), 2),
            'currency': 'USD',
            'details': 'Direct • Economy'
        })
        
    # --- TRAINS ---
    train_operators = ['Eurostar', 'TGV inOui', 'SNCF', 'Trenitalia', 'DB ICE', 'Frecciarossa']
    for i in range(random.randint(1, 3)):
        departure_hour = random.randint(5, 18)
        departure_min = random.choice([0, 10, 20, 30, 40, 50])
        dep_time = datetime.datetime.combine(travel_date, datetime.time(departure_hour, departure_min))
        
        duration_hrs = random.uniform(2.5, 6.0)
        duration_delta = datetime.timedelta(hours=duration_hrs)
        arr_time = dep_time + duration_delta
        
        options.append({
            'type': 'Train',
            'provider': random.choice(train_operators),
            'departure_time': dep_time.isoformat(),
            'arrival_time': arr_time.isoformat(),
            'duration': f"{int(duration_hrs)}h {int((duration_hrs % 1)*60)}m",
            'price_usd': round(random.uniform(30, 180), 2),
            'currency': 'USD',
            'details': 'High-Speed • 2nd Class'
        })

    # --- BUSES ---
    bus_operators = ['FlixBus', 'BlaBlaCar Bus', 'Megabus', 'Alsa']
    for i in range(random.randint(1, 2)):
        departure_hour = random.randint(7, 23)
        departure_min = random.choice([0, 15, 30, 45])
        dep_time = datetime.datetime.combine(travel_date, datetime.time(departure_hour, departure_min))
        
        duration_hrs = random.uniform(5.0, 12.0)
        duration_delta = datetime.timedelta(hours=duration_hrs)
        arr_time = dep_time + duration_delta
        
        options.append({
            'type': 'Bus',
            'provider': random.choice(bus_operators),
            'departure_time': dep_time.isoformat(),
            'arrival_time': arr_time.isoformat(),
            'duration': f"{int(duration_hrs)}h {int((duration_hrs % 1)*60)}m",
            'price_usd': round(random.uniform(15, 60), 2),
            'currency': 'USD',
            'details': 'Direct • Standard'
        })
        
    # Sort options by departure time
    options.sort(key=lambda x: x['departure_time'])
    
    return options
