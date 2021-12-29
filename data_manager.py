class DataManager:
    import requests
    low_price_data = "https://api.sheety.co/afb701dbd538b4bffbfec6887a823f2e/myFlightDeals/prices"

    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        results = self.requests.get(url=self.low_price_data)
        data = results.json()
        self.destination_data = data["prices"]
        return self.destination_data
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            responcse = self.requests.put(url=f"{self.low_price_data}/{city['id']}", json=new_data)
        # print(responcse.text)

    def get_user_emails(self):
        USERS_ENDPOINT = "https://api.sheety.co/afb701dbd538b4bffbfec6887a823f2e/myFlightDeals/users"
        response = self.requests.get(url=USERS_ENDPOINT)
        data = response.json()
        self.user_email = data["users"]
        return self.user_email