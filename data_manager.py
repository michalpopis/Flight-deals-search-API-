import requests

SHEETY_ENDPOINT = "SHEETY API"


class DataManager:
    #class is response to connect with Google sheet
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests(url=SHEETY_ENDPOINT)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_iatacodes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_ENDPOINT}/{city['id']}", json=new_data)
            print(response.text)

