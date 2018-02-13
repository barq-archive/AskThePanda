import pandas


class CityLoader:

    def __init__(self):
        pass

    def load_cities(self):

        df = pandas.read_csv('./static/resources/major_cities_csv.csv')

        return df['name'].values.tolist()