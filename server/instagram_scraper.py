import json
import requests
import datetime
from api_keys import igKey

def igLocSearch(clickPos):
    igApi = "https://api.instagram.com/v1/locations/search?access_token=" + igKey;

    # lat long from front end
    coordinates = clickPos.split(',')
    igLat = "&lat=" + coordinates[0];
    igLng = "&lng=" + coordinates[1];

    igLocQuery = igApi + igLat + igLng

    r = requests.get(igLocQuery)
    data = r.json()

    if data['meta']['code'] == 200:
        
        for location in data["data"]:
            print(location)

def main():
    igLocSearch("43.46858730253996,-79.69988822937012")


if __name__ == "__main__":
    main()