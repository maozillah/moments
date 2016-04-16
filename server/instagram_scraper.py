import json
import requests
import datetime
import math
from api_keys import igKey
RESULTS = {'moment': []}

def igLocSearch(clickPos):

    # clear data
    RESULTS["moment"] = []

    igApi = "https://api.instagram.com/v1/locations/search?access_token=" + igKey

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

    if data['meta']['code'] == 200 and data['data']:
        
        #check for closest location id
        for location in data["data"]:
            lat = location['latitude']
            lng = location['longitude']
            locID = location['id']

            # calculate each locID's distance to clickPos and add to store it
            locIDs[locID] = math.sqrt(math.pow(lat-float(currentLat),2) + math.pow(lng-float(currentLong),2))

        closestLocID = min(locIDs, key=locIDs.get)
        getLocPhotos(closestLocID)
    else:
        print('no Instagram locations nearby')
        RESULTS['moment'].append({'error' :'no Instagram locations nearby'})

    return RESULTS

def getLocPhotos(LocID):
    #TO DO Error handling
    igLocApi = "https://api.instagram.com/v1/locations/"
    LocIDQuery = igLocApi + LocID + "/media/recent?access_token=" + igKey

    igR = requests.get(LocIDQuery)
    igPhotos = igR.json()

    if igPhotos['meta']['code'] == 200 and igPhotos['data']:
        photo = igPhotos['data'][0]

        RESULTS['moment'].append({
            'img_url' : photo['images']['standard_resolution']['url'],
            'caption' : photo['caption']['text'],
            'tags' : photo['tags'],
            'url' : photo['link'],
            'lat' : photo['location']['latitude'],
            'long' : photo['location']['longitude']
        })
    else: 
        print('no instagram images nearby')
        RESULTS['moment'].append({'error' :'no instagram images nearby'})

# def main():
    # test with sheridan college location
    # igLocSearch("43.46858730253996,-79.69988822937012")

    #search no locations nearby
    # igLocSearch("20.3034175184893,-178.2421875")

if __name__ == "__main__":
    main()