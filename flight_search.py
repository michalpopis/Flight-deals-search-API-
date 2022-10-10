import requests
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = "YOUR_API_KEY_HERE"


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def get_destination_code(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": TEQUILA_API_KEY}
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, headers=headers, params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code

    def check_flight_price(self, city_from_code, city_to_code, from_time, to_time):
        search_endpoint = f"{TEQUILA_ENDPOINT}/v2/search"
        headers = {"apikey": TEQUILA_API_KEY}
        query = {
            "fly_from": city_from_code,
            "fly_to": city_to_code,
            "date_from": from_time,
            "date_to": to_time,
            "nights_in_dst_from": 3,
            "nights_in_dst_to": 7,
            "adults": 1,
            "flight_type": "round",
            "one_for_city": 1,
            "curr": "PLN",
            "max_stopovers": 0,
        }
        response = requests.get(url=search_endpoint, headers=headers, params=query)

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {city_to_code}")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["cityCodeFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["cityCodeTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_arrival"].split("T")[0],
            airline=data["route"][0]["airline"],
        )
        print(f"{flight_data.destination_city}: {flight_data.price} PLN")
        return flight_data
