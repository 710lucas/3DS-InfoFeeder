from dotenv import load_dotenv
import requests
import os
import psutil
import threading

import json

import system_data

def send_data(API_URL, API_PORT, payload):
    try:
        response = requests.post("http://"+API_URL+":"+API_PORT+"/", data=payload)

        #threading.Timer(1, send_data, args=(API_URL, API_PORT)).start()
    except Exception as e:
        print(e)

def loadSettings():
    with open("settings.json") as jsonFile:
        return json.load(jsonFile)
    
def getRequestString(settings):
    requestString = ""
    cpuEnabled = settings.get("cpu").get("enabled", False)
    cpu = settings.get("cpu", None)

    memoryEnabled = settings.get("memory").get("enabled", False)
    memory = settings.get("memory")

    diskEnabled = settings.get("disk").get("enabled", False)
    disk = settings.get("disk")

    if(cpuEnabled):
        requestString += system_data.getCPUData(
            graph = cpu.get("graph", True), 
            percentage = cpu.get("percentage", True)
        ) + "\n"
    
    if(memoryEnabled):
        requestString += system_data.getMemoryData(
            graph = memory.get("graph", True),
            active = memory.get("active", True),
            percentage = memory.get("percentage", True),
            total = memory.get("total", True)
        ) + "\n"

    if(diskEnabled):
        requestString += system_data.getDiskData(
            free= disk.get("free", True),
            usedTotal= disk.get("usedTotal", False),
            graph= disk.get("graph", True),
            percentage= disk.get("percentage", True)
        ) + "\n"

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