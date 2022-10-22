from twilio.rest import Client

account_sid = "Your Twilio Account SID"
auth_token = "Your Twilio Auth Token"


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def send_msg(self, price, origin_city, origin_airport, destination_city,
                 destination_airport, out_date, return_date, airline):
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"Low price alert! Only {price} PLN to fly from {origin_city}-{origin_airport} "
                 f"to {destination_city}-{destination_airport}, from {out_date} to {return_date} by {airline}.",
            from_="Phone number from twilio",
            to="Your phone number added in twilio"
        )
        print(message.status)

