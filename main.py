from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()

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
    