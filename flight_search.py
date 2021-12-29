import requests
from flight_data import FlightData

flight_data_endpoint = "https://tequila-api.kiwi.com"
API_KEY = "dVfLCK3zlalrlNK68Wzqe9pgYl1RfG_D"


# results = requests.get(url=flight_data_endpoint)


class FlightSearch:
    # This class is responsible for structuring the flight data.
    def get_destnation_code(self, city_name):
        location_endpoint = f"{flight_data_endpoint}/locations/query"
        headers = {"apikey": API_KEY}
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, headers=headers, params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code

    def check_flights(self, starting_city_code, destination_city_code, from_time, to_time, ):
        header = {
            "apikey": API_KEY
        }
        query = {
            "fly_from": starting_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        response = requests.get(f"{flight_data_endpoint}/v2/search", headers=header, params=query)

        try:
            data = response.json()["data"][0]
        except IndexError:
            query["max_stopovers"] = 1
            response = requests.get(f"{flight_data_endpoint}/v2/search", headers=header, params=query)
            try:
                data = response.json()["data"][0]

            except IndexError:
                pass
            else:
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][1]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"])
                return flight_data

        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            # print(f"{flight_data.destination_city}: £{flight_data.price}")
            return flight_data
