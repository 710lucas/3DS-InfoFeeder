import requests

def makeCall(url = None, body = None, objects = None, method = "GET"):
    if(url == None or objects == None):
        return
    
    data = {}
    if(body != None):
        data = body

    response = getattr(requests, method.lower())(url, data)

    returnData = ""

    if(response.status_code == 200):
        for o in objects:
            returnData += o.get("label")
            value = response.json()
            for v in o.get("value"):
                value = value.get(v)
            returnData += str(value) +"\n"
        
        return returnData
    return None


