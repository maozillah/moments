import json
import requests
import math

from random import randint
from api_keys import igKey
RESULTS = {'moment': []}

def igLocSearch(clickPos):
    igApi = "https://api.instagram.com/v1/locations/search?access_token=" + igKey

    # lat long from front end
    coordinates = clickPos.split(',')
    currentLat = coordinates[0]
    currentLong = coordinates[1]
    igLat = "&lat=" + currentLat
    igLng = "&lng=" + currentLong

    igLocQuery = igApi + igLat + igLng

    # keep track of location id for distance calculations
    locIDs = {}

    # clear data
    RESULTS["moment"] = []

    r = requests.get(igLocQuery)
    data = r.json()

    if data['meta']['code'] == 200 and data['data']:
        
        #check for closest location id
        for location in data["data"]:
            lat = location['latitude']
            lng = location['longitude']
            locID = location['id']

            # calculate each locID's distance to clickPos and add to store it
            locIDs[locID] = math.sqrt(math.pow(lat-float(currentLat),2) + math.pow(lng-float(currentLong),2))

        closestLocID = min(locIDs, key=locIDs.get)
        print(closestLocID)

        getLocPhotos(closestLocID)
    else:
        print('no Instagram locations nearby')
        RESULTS['moment'].append({'error' :'no Instagram locations nearby'})

    print(RESULTS)
    return RESULTS

def getLocPhotos(LocID):
    igLocApi = "https://api.instagram.com/v1/locations/"
    LocIDQuery = igLocApi + LocID + "/media/recent?access_token=" + igKey

    # global / local
    # numImgsUsed = 0

    igR = requests.get(LocIDQuery)
    igPhotos = igR.json()

    if igPhotos['meta']['code'] == 200 and igPhotos['data']:
        
        totalImgs = len(igPhotos['data'])

        # for photo in igPhotos['data']:
        #     print(photo['id'])

        # select random photo
        photo = igPhotos['data'][randint(0,totalImgs-1)]

        # photo = igPhotos['data'][1]
        # print("total images",totalImgs)
        # print("used images",numImgsUsed)

        # # check if photo has already used
        # if photo["id"] in open('usedImgs.txt').read():
        #     if totalImgs == numImgsUsed:
        #         print("images all used")
        #     else:
        #         print("already used this image")
        #         numImgsUsed += 1
        #         igPhotos['data'][randint(0,totalImgs)]

        #TODO: error handling if all images have been used

        if photo['caption']:
            RESULTS['moment'].append({
                'img_url' : photo['images']['standard_resolution']['url'],
                'caption' : photo['caption']['text'],
                'tags' : photo['tags'],
                'url' : photo['link'],
                'lat' : photo['location']['latitude'],
                'long' : photo['location']['longitude']
            })
        else:
            RESULTS['moment'].append({
                'img_url' : photo['images']['standard_resolution']['url'],
                'caption' : "no caption",
                'tags' : photo['tags'],
                'url' : photo['link'],
                'lat' : photo['location']['latitude'],
                'long' : photo['location']['longitude']
            })


        # add new image id to text file
        # with open('usedImgs.txt', 'a') as file:
        #     file.write(photo["id"]+",")
    else: 
        print('no instagram images nearby')
        RESULTS['moment'].append({'error' :'no instagram images nearby'})

def main():
    # test with sheridan college location
    igLocSearch("43.468314775456854,-79.69923913478851")

    # search no locations nearby
    # igLocSearch("20.3034175184893,-178.2421875")

if __name__ == "__main__":
    main()