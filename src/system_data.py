import os
import psutil


# Styles:
# percentage == True -> 50%
# activeTotal == True -> 8/16 GB
# graph == True -> [▮▮▮▮▮     ]
def getMemoryData(percentage = True, active = True, total = True, graph = True):
    returnData = ""
    mem = psutil.virtual_memory()

    returnData += "Memory: " 

    if(percentage):
        returnData += (str(mem.percent)+"% ").rjust(8)

    if(graph):
        returnData += "[".rjust(4)
        percent = mem.percent
        for i in range(10):
            if(percent >= i*10):
                returnData += "#"
            else:
                returnData += " "
        returnData += "] "

    if(active):
        active_amount = mem.active / (1024 ** 3)
        total_amount = mem.total / (1024 ** 3)
        if(total):
            returnData += f"{active_amount:.1f}/{total_amount:.1f} GB"
        if(active):
            returnData += f"{active_amount:.1f}GB"

    return returnData
        
def getCPUData(percentage = True, graph = True):
    returnData = ""
    percent = psutil.cpu_percent(interval=0.5)
    returnData += "CPU: "
    if(percentage):
        returnData += (str(percent) + "% ").rjust(11)
    
    if(graph):
        returnData += "[".rjust(4)
        for i in range(10):
            if(percent >= i*10):
                returnData += "#"
            else:
                returnData += " "
        returnData += "] "
    
    return returnData

def getDiskData(percentage = True, graph = True, free = True, usedTotal = False):
    returnData = ""
    diskUsage = psutil.disk_usage(path="/")
    percent = diskUsage.percent
    freeDisk = diskUsage.free / (1024 ** 3)
    used = diskUsage.used / (1024 ** 3)
    total = diskUsage.total / (1024 ** 3)

    returnData += "Disk: "
    if(percentage):
        returnData += f"{percent:.1f}% ".rjust(10)

    if(graph):
        returnData += "[".rjust(4)
        for i in range(10):
            if(percent >= i*10):
                returnData += "#"
            else:
                returnData += " "
        returnData += "] "
    
    if(free):
        returnData += f"{freeDisk:.2f} GB "
    
    if(usedTotal):
        returnData += f"{used:.2f}/{total:.2f} GB"

    return returnData

def getSystemData(item = "", args = {}):
    match(item):
        case "cpu":
            return getCPUData(
                graph = args.get("graph", True),
                percentage = args.get("percentage", True)
            ) 
        case "memory":
            return getMemoryData(
                graph = args.get("graph", True),
                active = args.get("active", True),
                percentage = args.get("percentage", True),
                total = args.get("total", True)
            ) 
        case "disk":
            return getDiskData(
                graph = args.get("graph", True),
                percentage = args.get("percentage", True),
                free = args.get("free", True),
                usedTotal = args.get("usedTotal", False)
            )
        case _:
            return ""