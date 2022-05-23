import requests

DOWNLOAD_LIMIT = 15

# Upper and lower bounds, i.e. aspect ratio is between 16:10 and 16:9 inclusive. Optimal for normal computer screens (I think?).
ASPECT_RATIO_LIMIT_MIN = 1.6
ASPECT_RATIO_LIMIT_MAX = 1.8

BASE_SEARCH_URL = 'https://collectionapi.metmuseum.org/public/collection/v1/search'
BASE_OBJECT_URL = 'https://collectionapi.metmuseum.org/public/collection/v1/objects'

# This is not a search engine, go to https://www.metmuseum.org/art/collection/search? to explore what given search parameters return.
# 'q': search text (e.g. 'mountains') works well for narrowing down.
# 
SEARCH_PARAMETERS = {"departmentId": "11", "q": "monet"}

search = requests.get(BASE_SEARCH_URL, params=SEARCH_PARAMETERS)
result = search.json()

if search.status_code == requests.codes.ok and result['total'] > 0:   
    for item in result['objectIDs']:
        object = requests.get(BASE_OBJECT_URL + '/' + str(item))
        object_json = object.json()

        if object.status_code == requests.codes.ok:
            # API returns {'message': 'Not Found'} if object is not found. Otherwise, it returns the object.
            # i.e. iff object contains key 'message' then fetching object has failed.
            if not "message" in object_json and "measurements" in object_json and "primaryImage" in object_json and object_json["isPublicDomain"]:
                try:
                    h = object_json['measurements'][0]['elementMeasurements']['Height']
                    w = object_json['measurements'][0]['elementMeasurements']['Width']
                except: 
                    print("Could not parse dimensions for object#" + str(item) + ". Continuing.")
                    continue

                if w/h > ASPECT_RATIO_LIMIT_MIN and w/h < ASPECT_RATIO_LIMIT_MAX:
                    # object_json['primaryImage'] has the URL of the image. Download the image.
                    image = requests.get(object_json['primaryImage'])
                    with open(object_json['title'].replace(" ", "") + '.jpg', 'wb') as f:
                        f.write(image.content)
                    print('Downloaded image for object #' + str(item) + '.')
                    DOWNLOAD_LIMIT -= 1

                    if DOWNLOAD_LIMIT == 0:
                        print("Download limit reached. Exiting.")
                        quit()
                    
        else:
            print("Could not fetch object {0}.".format(item))    
else:
    print("SEARCH URL Error. Exiting.")            
    quit()
