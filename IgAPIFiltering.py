import json, datetime, time, re, requests 

pages = "["
yourClientId = "XXX"
location = "604145"#Rag and Famish North Sydney!
api = "https://api.instagram.com/v1/locations/{0}/media/recent?client_id={1}".format(location,yourClientId)
while True:
    r = requests.get(api)
    instagramEnvelope =  r.json();
    pagination = instagramEnvelope["pagination"]
    if not pagination:
        pages = pages[:-1]
        break
    pages += r.text
    pages += ","
    api = pagination["next_url"]
pages += "]"



def iterateWay(igUserToFind):
    pagesArray = json.loads(pages)
    for page in pagesArray:
        for location in page["data"]:
            if location["user"]["id"] == igUserToFind:
                print(datetime.datetime.fromtimestamp(int(location["created_time"])).strftime('%Y-%m-%d %H:%M:%S'))

   
                        
def regexWay(igUserToFind):
    p = re.compile(r'"user":\s*({[^}]*(("'+igUserToFind+'"))[^}]*})',re.DOTALL)
    for found in re.finditer(p,pages):
        location = getLocationObject(found.end())
        print(datetime.datetime.fromtimestamp(int(location["created_time"])).strftime('%Y-%m-%d %H:%M:%S'))       

def getLocationObject(index):
    retentionCount = -1
    while retentionCount != 0:
        if pages[index] == "}":
            retentionCount += 1
        elif pages[index] == "{":
            retentionCount -= 1
        index += 1
    index -= 1;
    endIndex = index
    while True:
        if pages[index] == "}":
            retentionCount += 1
        elif pages[index] == "{":
            retentionCount -= 1
        index -= 1
        if retentionCount == 0:
            break
    startIndex = index + 1
    objectJson = pages[startIndex:endIndex +1]
    return json.loads(objectJson)

 
def timeIterateWay(igUserToFind):
    startTime = time.time()
    iterateWay(igUserToFind)
    print time.time() - startTime, "seconds for iteration"

def timeRegexWay(igUserToFind):
    startTime = time.time()
    regexWay(igUserToFind)
    print time.time() - startTime, "seconds for regex"

igUserToFind = "3419631"
timeRegexWay(igUserToFind)
timeIterateWay(igUserToFind)
