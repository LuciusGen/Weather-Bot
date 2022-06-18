import json
import os


class CitiesLoader:
    def __init__(self, directory, json_name):
        self.cities = []
        os.chdir(directory)
        with open(json_name, encoding='utf-8', mode='r') as json_file:
            cities_file = json.loads(json_file.read())
            for i in cities_file:
                self.cities.append(i['city'])


if __name__ == '__main__':
    loader = CitiesLoader("../resources", "russia.json")
    print(loader.cities)