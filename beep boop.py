from tkinter import *
from image_util import *
import requests
import json
import time
import datetime
from math import sin, cos, sqrt, atan2, radians, acos
import mpu  
import string

def getIPAddress(): 
    return requests.get('http://ip.42.pl/raw').text
    
def getYourLocation(IPAddress): 
    sendUrl = 'https://api.ipgeolocation.io/ipgeo?apiKey=c93af7c4fa124aa2b6894964005f9333' 
    r = requests.get(sendUrl)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    return [float(lat), float(lon)]

def getBeepBoopRotations(timeStart): 
    #Note this is in seconds
    beepBoopDuration = 28
    beepBoopLength = 135 
    beepBoopLst = []  
    for i in range(timeStart, 86400, 163):
        beepBoopLst.append(i)
    for j in range(0, timeStart, 163):
        beepBoopLst.append(j)
    return beepBoopLst
    
def findBeepBoopTime(extraTime):
    beepBoopLocation = (40.444638, -79.9430)
    cTime = str(datetime.datetime.now().time())
    cTime = cTime[0:8]
    
    x = time.strptime(cTime.split(',')[0],'%H:%M:%S')
    cTimeSeconds = (datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds())
    #Calculate distance that it takes 
    #Give the pace that you take, how long will it take. 
    #Compare your time to the nearest on
    
    timeRanges = getBeepBoopRotations(28828)
    timeRanges.sort()
    for times in timeRanges:
        if times - extraTime - cTimeSeconds > 0:
            beepBoopHours = str(((times) // 3600))
            if int(beepBoopHours) > 12:
                beepBoopHours = str(int(beepBoopHours) % 12)
            beepBoopMinutes = str(((times) / 3600) % int(beepBoopHours) * 60 // 1)[:-2]
            beepBoopSeconds = str((((times) / 3600) % int(beepBoopHours) * 60) % int(beepBoopMinutes) * 60 // 1)[:-2]
            if len(beepBoopHours) == 1:
                beepBoopHours = "0" + beepBoopHours
            if len(beepBoopMinutes) == 1:
                beepBoopMinutes = "0" + beepBoopMinutes
            if len(beepBoopSeconds) == 1:
                beepBoopSeconds = "0" + beepBoopSeconds
            hours = str((times - extraTime) // 3600)[:-2]
            if int(hours) > 12:
                hours = str(int(hours) % 12)
            minutes = str(((times - extraTime) / 3600) % int(hours) * 60 // 1)[:-2]
            seconds = str((((times - extraTime) / 3600) % int(hours) * 60) % int(minutes) * 60 // 1)[:-2]
            if len(hours) == 1:
                hours = "0" + hours
            if len(minutes) == 1:
                minutes = "0" + minutes
            if len(seconds) == 1:
                seconds = "0" + seconds
            return beepBoopHours + ":" + beepBoopMinutes + ":" + beepBoopSeconds, hours + ":" + minutes + ":" + seconds
    
    
def feetToTime(distance, speed):
    return distance / speed

def findDistance(currentLocation, hub):
    slat = radians(currentLocation[0])
    slon = radians(currentLocation[1])
    elat = radians(hub[0])
    elon = radians(hub[1])
    
    dist = 6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
    return dist * 3280.84

def findClosestHub(currentLocation):
    dictOfHubsToBeepBoop = {"Wean": 1679, 
                            "Doherty": 1151,
                            "schoolDrama": 584,
                            "Warner": 285,
                            "Porter": 1817,
                            "BakerHall": 1161,
                            "Scaife": 1833,
                            "Gates": 626,
                            "CFA": 997,
                            "UC": 620,
                            "ABP": 338,
                            "Resnik": 1748,
                            "Entropy": 902,
                            "Rez": 2329,
                            "Fifth & Morewood intersection": 1106,
                            "Mudge": 1086,
                            "Stever": 558,
                            "ETower": 174,
                            "Fairfax": 2333,
                            "Neville Apartments": 2487,
                            "Webster": 3161,
                            "Shirley": 3480}
                
    dictOfYouToHubs = {"WEAN": (40.442391, -79.946019), 
                    "DOHERTY": (40.441958, -79.943949), 
                    "SCHOOLDRAMA": (40.443093, -79.943457),
                    "WARNER": (40.443901, -79.943151), 
                    "PORTER": (40.442092, -79.946094), 
                    "BAKERHALL": (40.441651, -79.944043),
                    "SCAIFE": (40.441547, -79.947000), 
                    "GATES": (40.443593, -79.944445),
                    "CFA": (40.442043, -79.942999), 
                    "UC": (40.443150, -79.942648), 
                    "ABP": (40.444140, -79.942271), 
                    "RESNIK": (40.442339, -79.939893), 
                    "ENTROPY": (40.44280, -79.941946), 
                    "RESIDENCE ON FIFTH": (40.446967, -79.946800), 
                    "MOREWOOD": (40.447417, -79.942524),
                    "MUDGE": (40.447019, -79.942392),
                    "STEVER": (40.446246, -79.942260),
                    "ETOWER": (40.445000, -79.942820),
                    "FAIRFAX": (40.446994, -79.948167),
                    "NEVILLE APARTMENTS": (40.447468, -79.947374),
                    "WEBSTER": (40.447009, -79.950682),
                    "SHIRLEY": (40.447825, -79.951166)}

    smallestDistance = None
    smallestDistanceName = None
    for possHub in dictOfYouToHubs:
        latLonHub = dictOfYouToHubs[possHub]
        distanceYou2Hub = findDistance(currentLocation, latLonHub)
        if smallestDistance == None or  distanceYou2Hub <= smallestDistance:
            smallestDistance = distanceYou2Hub
            smallestDistanceName = possHub
    return distanceHub2BeepBoop((smallestDistanceName, smallestDistance))
    
def distanceHub2BeepBoop(smallestNameDist):
    dictOfHubsToBeepBoop = {"WEAN": 1679, 
                            "DOHERTY": 1151,
                            "SCHOOLDRAMA": 584,
                            "WARNER": 285,
                            "PORTER": 1817,
                            "BAKER HALL": 1161,
                            "SCAIFE": 1833,
                            "GATES": 626,
                            "CFA": 997,
                            "UC": 620,
                            "AU BON PAIN": 338,
                            "RESNIK": 1748,
                            "ENTROPY": 902,
                            "RESIDENCE ON FIFTH": 2329,
                            "MUDGE": 1086,
                            "STEVER": 558,
                            "MOREWOOD": 174,
                            "FAIRFAX": 2333,
                            "NEVILLE APARTMENTS": 2487,
                            "WEBSTER": 3161,
                            "SHIRLEY": 3480}
    place = smallestNameDist[0]
    dist = smallestNameDist[1]
    totalDist = dist + dictOfHubsToBeepBoop[place]
    return place, totalDist

def init(data):
    data.title = True
    data.menuSelect = False
    data.inputLocation = False
    data.timeScreen = False
    data.textInput = ""
    data.inputInstructions = "Type your current location. Use the following list as guide:"
    data.step = 0
    data.listOfPlaces = []
    data.timer = 0
    data.blink = True
    data.cloud = PhotoImage(file = "cloud.png")
    data.cloud1X = 0
    data.cloud2X = 100
    data.distances = {"WEAN": 1679, 
                            "DOHERTY": 1151,
                            "SCHOOLDRAMA": 584,
                            "WARNER": 285,
                            "PORTER": 1817,
                            "BAKER HALL": 1161,
                            "SCAIFE": 1833,
                            "GATES": 626,
                            "CFA": 997,
                            "UC": 620,
                            "ABP": 338,
                            "RESNIK": 1748,
                            "ENTROPY": 902,
                            "RESIDENCE ON FIFTH": 2329,
                            "MUDGE": 1086,
                            "STEVER": 558,
                            "MOREWOOD": 174,
                            "FAIRFAX": 2333,
                            "NEVILLE APARTMENTS": 2487,
                            "WEBSTER": 3161,
                            "SHIRLEY": 3480}

def mousePressed(event, data):
    if data.title  == True:
        if event.x >= data.width / 2 - 55 and event.x <= data.width / 2 + 55 and event.y >= data.height / 2 - 35 and event.y <= data.height / 2 + 75:
            data.menuSelect = True
            data.title = False
            data.speed = 7.10
        elif event.x >= data.width / 2 - 55 and event.x <= data.width / 2 + 55 and event.y >= data.height / 2 + 80 and event.y <= data.height / 2 + 190:
            data.menuSelect = True
            data.title = False
            data.speed = 4.55
        elif event.x >= data.width / 2 - 55 and event.x <= data.width / 2 + 55 and event.y >= data.height / 2 + 195 and event.y <= data.height / 2 + 305:
            data.menuSelect = True
            data.title = False
            data.speed = 2.35
            
    elif data.menuSelect:
        data.title = False
        if event.x >= data.width / 2 - 100 and event.y >= data.height / 4 - 100 and event.x <= data.width / 2 + 100 and event.y <= data.height / 4 + 100:
            data.inputLocation = False
            data.hub = findClosestHub(getYourLocation(getIPAddress()))[0]
            data.beepBoopTime = findBeepBoopTime(feetToTime(findClosestHub(getYourLocation(getIPAddress()))[1], data.speed))[0]
            data.finalTime = findBeepBoopTime(feetToTime(findClosestHub(getYourLocation(getIPAddress()))[1], data.speed))[1]
            data.timeScreen = True
            data.menuSelect = False
        elif event.x >= data.width / 2 - 100 and event.y >= data.height / 4 * 3 - 100 and event.x <= data.width / 2 + 100 and event.y <= data.height / 4 * 3 + 100:
            data.useCurrentLocation = False
            data.inputLocation = True
            data.menuSelect = False
        
def timerFired(data):
    data.timer += .1
    if data.timer % 3 == 0:
        data.blink = not data.blink
    data.cloud1X += 5
    data.cloud2X += 8
    if data.cloud1X - 62.5 >= data.width:
        data.cloud1X = -62.5
    if data.cloud2X - 62.5 >= data.width:
        data.cloud2X = -62.5
    

def keyPressed(event, data):
    if event.keysym == "Escape":
        data.title = True
        data.inputLocation = False
        data.timeScreen = False
        data.textInput = ""
        data.inputInstructions = "Type your current location. Use the following list as guide:"
    if data.inputLocation:
        data.validLocation = False
        if event.keysym.upper() in string.ascii_letters:
            data.textInput += event.keysym.upper()
        elif event.keysym == "space":
            data.textInput += " "
        elif event.keysym == "BackSpace":
            data.textInput = data.textInput[:-1]
        elif event.keysym == "Return":
            for key in data.distances:
                if key == data.textInput:
                    data.validLocation = True
                    data.currentDistance = data.distances[key]
            if data.validLocation:
                data.hub = data.textInput
                data.finalTime = findBeepBoopTime(feetToTime(data.currentDistance, data.speed))[1]
                data.beepBoopTime = findBeepBoopTime(feetToTime(data.currentDistance, data.speed))[0]
                data.inputLocation = False
                data.timeScreen = True
            else:
                data.inputInstructions = "Invalid location. Please retype your location."
                data.textInput = ""

def redrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "light cyan", width = 0)
    if data.title:
        canvas.create_image(data.cloud1X, 60, image = data.cloud)
        canvas.create_image(data.cloud2X, 110, image = data.cloud)
        canvas.create_text(data.width / 2, 80, text = " Catch the \nBeep Boop", font = "Helvetica 50 bold", anchor = "n")
        canvas.create_rectangle(data.width / 2 - 65, data.height / 2 - 50, data.width / 2 + 65, data.height - 35, fill = "black")
        canvas.create_oval(data.width / 2 - 55, data.height / 2 - 35, data.width / 2 + 55, data.height / 2 + 75, fill = "red")
        canvas.create_oval(data.width / 2 - 55, data.height / 2 + 80, data.width / 2 + 55, data.height / 2 + 190, fill = "gold")
        canvas.create_oval(data.width / 2 - 55, data.height / 2 + 195, data.width / 2 + 55, data.height / 2 + 305, fill = "lime green")
        canvas.create_text(data.width / 2, data.height / 2 + 15, text = "     Super \nSpeed Walk", font = "Times 20 bold")
        canvas.create_text(data.width / 2, data.height / 2 + 135, text = "    Casual \nSpeed Walk", font = "Times 20")
        canvas.create_text(data.width / 2, data.height / 2 + 250, text = "    Super \nSlow Walk", font = "Times 20 italic")
        data.personWalking = PhotoImage(file = "walking-man.png")
        if data.blink:
            canvas.create_image(data.width / 6, data.height / 3 * 2, image = data.personWalking)
            canvas.create_image(data.width / 6 * 5, data.height / 3 * 2, image = data.personWalking)
        
    elif data.inputLocation:
        canvas.create_text(data.width / 2, data.height / 4, text = data.inputInstructions, font = "Helvetica 15 bold")
        canvas.create_text(data.width / 2, data.height / 2, text = data.textInput, font = "Helvetica 50 bold")
        canvas.create_text(data.width / 5, 600, text = "Wean\nWarner\nScaife\nUC\nEntropy\nStever\nNeville Apartments", font = "Helvetica 16")
        canvas.create_text(data.width / 2, 600, text = "Doherty\nPorter\nGates\nABP\nResidence On Fifth\nMorewood\nWebster", font = "Helvetica 16")
        canvas.create_text(data.width / 4 * 3, 600, text = "Schooldrama\nBaker Hall\nCFA\nResnik\nMudge\nFairfax\nShirley", font = "Helvetica 16")
            
            
            
    elif data.menuSelect:
        canvas.create_oval(data.width / 2 - 100, data.height / 4 - 100, data.width / 2 + 100, data.height / 4 + 100, fill = "orange", width = 5)
        canvas.create_text(data.width / 2, data.height / 4, text = "Use Current Location", font = "Helvetica 18 bold")
        canvas.create_oval(data.width / 2 - 100, data.height / 4 * 3 - 100, data.width / 2 + 100, data.height / 4 * 3 + 100, fill = "orange", width = 5)
        canvas.create_text(data.width / 2, data.height / 4 * 3, text = "Type Nearest Location", font = "Helveitca 18 bold ")
    elif data.timeScreen:
        data.map = PhotoImage(file = data.hub + ".png")
        canvas.create_image(data.width / 2, 100, anchor = N, image = data.map)
        canvas.create_text(data.width / 2, data.height / 4 * 3, text = "Beep Boop at: " + data.beepBoopTime, font = "Helvetica 20 bold")
        canvas.create_text(data.width / 2, data.height / 4 * 3.5, text = "Leave at: " + data.finalTime, font = "Helvetica 20 bold")
        
    

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(500, 700)