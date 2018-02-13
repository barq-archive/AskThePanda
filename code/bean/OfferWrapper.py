import json


class OfferWrapper:
    country = ""
    currency = ""
    language = ""
    check_in = ""
    check_out = ""
    offer_list = []

    def __init__(self):
        pass

    def toJSON(self):
        return json.dumps(self, default=lambda item: item.__dict__,
                          sort_keys=True, indent=4)