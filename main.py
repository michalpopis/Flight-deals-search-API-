from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
message = NotificationManager()

ORIGIN_CITY_IATA = "Your City IATA Code"

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_iatacodes()

tomorrow = datetime.now() + timedelta(days=1)
in_six_months = datetime.now() + timedelta(days=183)

for destination in sheet_data:
    flight = flight_search.check_flight_price(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow.strftime("%d/%m/%Y"),
        to_time=in_six_months.strftime("%d/%m/%Y"),
    )
    if flight and flight.airline == "FR":
        if destination["lowestPrice"] > flight.price:
            message.send_msg(flight.price, flight.origin_city, flight.origin_airport, flight.destination_city,
                             flight.destination_airport, flight.out_date, flight.return_date, airline="RyanAir")
    elif flight and flight.airline == "W6":
        if destination["lowestPrice"] > flight.price:
            message.send_msg(flight.price, flight.origin_city, flight.origin_airport, flight.destination_city,
                             flight.destination_airport, flight.out_date, flight.return_date, airline="WizzAir")
    else:
        if flight and destination["lowestPrice"] > flight.price:
            message.send_msg(flight.price, flight.origin_city, flight.origin_airport, flight.destination_city,
                             flight.destination_airport, flight.out_date, flight.return_date, flight.airline)
                             