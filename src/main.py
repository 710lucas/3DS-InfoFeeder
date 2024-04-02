from dotenv import load_dotenv
import requests
import os
import psutil
import threading
from collections import OrderedDict

import json

import system_data
import api_calls

def send_data(API_URL, API_PORT, payload):
    try:
        response = requests.post("http://"+API_URL+":"+API_PORT+"/", data=payload)

        #threading.Timer(1, send_data, args=(API_URL, API_PORT)).start()
    except Exception as e:
        print(e)

def loadSettings():
    with open("settings.json") as jsonFile:
        return json.load(jsonFile, object_pairs_hook=OrderedDict)
    

def loadCustomMessage(customMessage):
    fullMessage = ""

    foregroundColors = {
        "black" : "\033[30m",
        "red" : "\033[31m",
        "green" : "\033[32m",
        "yellow" : "\033[33m",
        "blue" : "\033[34m",
        "magenta" : "\033[35m",
        "cyan" : "\033[36m",
        "white" : "\033[37m",
    }
    backgroundColors = {
        "black" : "\033[40m",
        "red" : "\033[41m",
        "green" : "\033[42m",
        "yellow" : "\033[43m",
        "blue" : "\033[44m",
        "magenta" : "\033[45m",
        "cyan" : "\033[46m",
        "white" : "\033[47m",
    }

    fullMessage+=backgroundColors.get(customMessage.get("bg-color"), "")
    fullMessage+=foregroundColors.get(customMessage.get("fg-color"), "")

    for line in customMessage.get("lines"):
        fullMessage += line + "\n"
    return fullMessage + "\033[0m"
    
def getRequestString(settings):
    requestString = ""

    systemInfo = ["cpu", "memory", "disk"]

    for key, value in settings.items():
        if (key in systemInfo):
            requestString += system_data.getSystemData(key, value) + "\n"
        if ("custom-message" in key):
            requestString += str(loadCustomMessage(value)).encode("ascii", errors="ignore").decode("ascii")
        if (key == "api-calls"):
            for api_call in value:
                requestString += str(api_calls.makeCall(api_call.get("url"), api_call.get("body", ""), api_call.get("objects")))


    return requestString

def doRequest(API_URL, API_PORT, settings):
    send_data(API_URL, API_PORT, getRequestString(settings))
    threading.Timer(2, doRequest, args=(API_URL, API_PORT, settings)).start()


load_dotenv(),

API_URL = os.getenv("API_URL")
API_PORT = os.getenv("API_PORT")

if(API_URL == None):
    API_URL = input("3DS server URL: ")

if(API_PORT == None):
    API_PORT = input("3DS server PORT: ")

settings = loadSettings()

doRequest(API_URL, API_PORT, settings)


# send_data(API_URL, API_PORT)
        
# print(system_data.getMemoryData(total = False))
# print(system_data.getCPUData())
# print(system_data.getDiskData())