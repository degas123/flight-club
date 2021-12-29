from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

dm = DataManager()
sheet_data = dm.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

STARTING_CITY_CODE = "LON"

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destnation_code(row["city"])
    print(sheet_data)
    dm.destination_data = sheet_data
    dm.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.check_flights(
        STARTING_CITY_CODE,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    if flight is None:
        continue

    if flight.price < destination["lowestPrice"]:
        users = dm.get_user_emails()
        emails = [row["email"]for row in users]
        name =[row["firstName"]for row in users]

        message = f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."

        if flight.stop_overs > 0:
            message += f'\nFlight has{flight.stop_overs} stop over, via {flight.via_city}'
            print(message)
        link=f"https://www.google.co.uk/flights?hl=en#flt=" \
             f"{flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}." \
             f"{flight.origin_airport}.{flight.return_date}"
        notification_manager.send_emails(emails,message,link)
