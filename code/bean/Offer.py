
class Offer:
    hotel_name = ""
    hotel_destination = ""
    hotel_lat = ""
    hotel_long = ""
    average_price = ""
    original_price_night = ""
    hotel_image = ""
    hotel_star = ""

    def __init__(self):
        pass


    def __init__(self, hotel_name, hotel_destination, hotel_lat, hotel_long, average_price, original_price, hotel_image, hotel_star):
        self.hotel_name = hotel_name
        self.hotel_destination = hotel_destination
        self.hotel_lat = hotel_lat
        self.hotel_long = hotel_long
        self.average_price = average_price
        self.original_price_night = original_price
        self.hotel_image = hotel_image
        self.hotel_star = hotel_star