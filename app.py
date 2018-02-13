import sys
from flask import Flask, request, render_template, jsonify
from code.controls.OffersLoader import OffersLoader
from code.controls.CityLoader import CityLoader
from code.util import Validator
from code.util.InvalidUsage import InvalidUsage
import urllib
import code.util.Helper as helper
import json

TESTING_MODE = False

app = Flask(__name__)
major_cities = CityLoader().load_cities()

@app.route("/")
def main():

    # load about
    about_list = helper.load_text_data('./static/resources/about.txt')
    about_data = {'title': about_list[0],'slogan':about_list[1],'info':about_list[2]}

    return render_template("index.html", cities=major_cities, about_data=about_data)


@app.route("/hoteloffers", methods=['POST'])
def hotel_offers():

    dist = request.form['dist']
    checkin = request.form['checkin']
    checkout = request.form['checkout']

    print("destination: ", dist)
    print("check-in: ", checkin)
    print("check-out: ", checkout)

    if Validator.validate_search(dist, checkin, checkout):

        # 1- load data and Parse data
        offer_wrapper = None
        try:
            loader = OffersLoader(dist, start_date=checkin, end_date=checkout)
            if TESTING_MODE:
                json_data = loader.load_testing()
            else:
                json_data = loader.load_data()

            offer_wrapper = loader.parse_data(json_data)

        except urllib.error.HTTPError as err:
            print(err)
            raise InvalidUsage('API Error', status_code=410)
        except:
            raise InvalidUsage('Server Error', status_code=410)

        # 3- prepare & return results
        json_result = offer_wrapper.toJSON()

        return json_result

    else:
        raise InvalidUsage('Input Validation Error', status_code=410)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')