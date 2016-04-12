import json
import requests
import datetime
import math
from api_keys import igKey

def igLocSearch(clickPos):
    igApi = "https://api.instagram.com/v1/locations/search?access_token=" + igKey;

    # lat long from front end
    coordinates = clickPos.split(',')
    currentLat = coordinates[0]
    currentLong = coordinates[1]
    igLat = "&lat=" + currentLat
    igLng = "&lng=" + currentLong

    igLocQuery = igApi + igLat + igLng

    r = requests.get(igLocQuery)
    data = r.json()

    locIDs = {}

    if data['meta']['code'] == 200:
        
        #check for closest location id
        for location in data["data"]:
            lat = location['latitude']
            lng = location['longitude']
            locID = location['id']

            # calculate each locID's distance to clickPos and add to store it
            locIDs[locID] = math.sqrt(math.pow(lat-float(currentLat),2) + math.pow(lng-float(currentLong),2));
    else:
        print("no locations nearby")

    closestLocID = min(locIDs, key=locIDs.get)
    getLocPhotos(closestLocID)

def getLocPhotos(LocID):
    igLocApi = "https://api.instagram.com/v1/locations/";
    LocIDQuery = LocID + "/media/recent?access_token=" + igKey

def main():
    igLocSearch("43.46858730253996,-79.69988822937012")


if __name__ == "__main__":
    main()