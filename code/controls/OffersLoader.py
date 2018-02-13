import httplib2
from code.util import Constants
import json
import urllib
import re
from code.bean.OfferWrapper import OfferWrapper
from code.bean.Offer import Offer


class OffersLoader:
    def __init__(self, city, start_date=None, end_date=None, product_type="Hotel", version=1):

        #assert city != None, "Country variable cant be null or empty"

        # create base url
        self.base_link = Constants.BASE_URL.replace("<uid>", Constants.UID).replace("<type>", product_type)

        # add city to search for it
        if city is not None and len(city.strip()) > 0:
            # filter non word
            city = re.sub(r'[^\w]', ' ', city.strip())
            # combine city with url
            self.base_link = self.base_link + "&" + Constants.DIST + "=" + urllib.parse.quote(city)

        # add date to search
        if start_date is not None and len(start_date.strip()) > 0:
            # combine date with url
            self.base_link = self.base_link + "&" + Constants.START_DATE + "=" + start_date

        if end_date is not None and len(end_date.strip()) > 0:
            # combine date with url
            self.base_link = self.base_link + "&" + Constants.END_DATE + "=" + end_date


    def load_data(self):
        print("Load URL: ", self.base_link)

        #req = urllib.request.Request(self.base_link, headers = {'User-agent': 'panda advisor bot by ahmad v0.1'})
        req = urllib.request.Request(self.base_link, headers={'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0'})

        json_data = json.load(urllib.request.urlopen(req))

        return json_data




    def load_testing(self):
        json_data = json.load(open('./static/resources/dummy_data.json'))

        return json_data

    def parse_data(self, json_data):
        print('calling parse data')

        offer_wrapper = OfferWrapper()

        print('currency test: ' , json_data['offerInfo']['currency'])

        offer_wrapper.currency = json_data['offerInfo']['currency']
        offer_wrapper.country  = json_data['offerInfo']['userSelectedCurrency']
        offer_wrapper.language = json_data['offerInfo']['language']

        offer_object = json_data['offers']

        if offer_object is not None and len(offer_object) > 0:
            offers_json = offer_object["Hotel"]

            hotel_list = []
            for offer in offers_json:
                print('parsing:: ' , offer['hotelInfo']['hotelName'])

                hotel_name = offer['hotelInfo']['hotelName']
                hotel_destination = offer['hotelInfo']['hotelDestination']
                hotel_lat = offer['hotelInfo']['hotelLatitude']
                hotel_long = offer['hotelInfo']['hotelLongitude']
                hotel_image = offer['hotelInfo']['hotelImageUrl']
                average_price = offer['hotelPricingInfo']['averagePriceValue']
                original_price = offer['hotelPricingInfo']['originalPricePerNight']
                hotel_star = offer['hotelInfo']['hotelStarRating']

                offer_bean = Offer(hotel_name, hotel_destination, hotel_lat, hotel_long, average_price, original_price, hotel_image, hotel_star)
                hotel_list.append(offer_bean)

            offer_wrapper.offer_list = hotel_list

        return offer_wrapper
