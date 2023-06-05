import requests

print("Enter download limit:")
DOWNLOAD_LIMIT = eval(input())
if DOWNLOAD_LIMIT < 1:
    DOWNLOAD_LIMIT = 1

# Upper and lower bounds, i.e. aspect ratio is between 16:10 and 16:9 inclusive. Optimal for normal computer screens (I think?).
ASPECT_RATIO_LIMIT_MIN = 1.6
ASPECT_RATIO_LIMIT_MAX = 1.8

BASE_SEARCH_URL = 'https://collectionapi.metmuseum.org/public/collection/v1/search'
BASE_OBJECT_URL = 'https://collectionapi.metmuseum.org/public/collection/v1/objects'

# Get search parameters from user.
print("Enter search text (i.e. \'landscape\', \'Van Gogh\') or press enter for default:")
search_text = input()

if search_text == "":
    # Default search text.
    search_text = "monet"


print("Press enter to filter by \'European Paintings\' or any key then enter to show department options.")
department_text = input()

if department_text == "":
    # Default department.
    department_text = "11"
else:
    deps = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/departments")
    deps_json = deps.json()
    for x in deps_json['departments']:
        print("%s: %s" % (x["displayName"], x["departmentId"]))
    department_text = input("Enter the number of the desired depeartment:\n")

# This is not a search engine, go to https://www.metmuseum.org/art/collection/search? to explore what given search parameters return.
# departmentID is by default set to 11 which is "European Paintings". See <https://collectionapi.metmuseum.org/public/collection/v1/departments>
# for a list of departments with thier corresponding int identifiers to change this.
SEARCH_PARAMETERS = {"departmentId": department_text, "q": search_text}
print("Working...")
search = requests.get(BASE_SEARCH_URL, params=SEARCH_PARAMETERS)
# Convert search result to JSON format. Result is a JSON containing the objectIDs for the search results.
result = search.json()
i = 0
print("%s objects found with given parameters. Checking for open access and suitable aspect ratio..." % result["total"])
if search.status_code == requests.codes.ok and result['total'] > 0:   
    for item in result['objectIDs']:
        # Get object details information.
        object = requests.get(BASE_OBJECT_URL + '/' + str(item))
        object_json = object.json()

        if object.status_code == requests.codes.ok:
            # API returns {'message': 'Not Found'} if object is not found. Otherwise, it returns the object.
            # i.e. iff object contains key 'message' then fetching object has failed.
            if not "message" in object_json and object_json["classification"] == "Paintings" and "measurements" in object_json and "primaryImage" in object_json and object_json["isPublicDomain"]:
                try:
                    h = object_json['measurements'][0]['elementMeasurements']['Height']
                    w = object_json['measurements'][0]['elementMeasurements']['Width']
                except: 
                    print("Could not parse dimensions for object #" + str(item) + ". Continuing.")
                    continue

                if w/h > ASPECT_RATIO_LIMIT_MIN and w/h < ASPECT_RATIO_LIMIT_MAX:
                    # object_json['primaryImage'] has the URL of the image. Download the image.
                    image = requests.get(object_json['primaryImage'])
                    with open(object_json['title'].replace(" ", "") + '.jpg', 'wb') as f:
                        f.write(image.content)
                    print('Downloaded image for object #' + str(item) + '.')
                    DOWNLOAD_LIMIT -= 1
                    i += 1

                    if DOWNLOAD_LIMIT == 0:
                        print("Download limit reached. Exiting.")
                        quit()
                    
        else:
            print("Could not fetch object #{0}, continuing.".format(item))    

    print("COMPLETE.")
    print("\nChecked %s objects from search result. \nDownloaded the %d images which passed filters." % (result["total"], i))
else:
    print("SEARCH URL Error. Exiting.")            
    quit()
