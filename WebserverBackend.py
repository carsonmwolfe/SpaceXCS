# SpaceX CS Project Backend
# Last Updaed December 4th
import flask
import datetime
import requests
import json
import os
from typing import Dict
import logging

#from . import spacex


app=flask.Flask(__name__)

@app.route('/')
#Home Page
def index():
    return flask.render_template('index.html')

@app.route('/countdown')
def countdown():

    Latest = requests.get("https://api.spacexdata.com/v4/launches/latest").text
    json_Latest=json.loads(Latest)
    Upcoming = requests.get("https://api.spacexdata.com/v4/launches/upcoming").text
    json_Upcoming=json.loads(Upcoming)
    countdowntimer = str(json_Upcoming[0]["date_local"])
    now = datetime.datetime.now()
    liftoff = str(now)
    countdowntimer = str(json_Upcoming[0]["date_local"])
    s = countdowntimer.split('T')
    a = s[0].split('-')
    t = s[1].split('-')
    u = t[0].split(',')
    v = u[0].split(':')
    launch = a + v
    launchtime = []
    for e in launch:
        launchtime.append(int(e))

    launchtime[3]=launchtime[3]-4
    launchdatetime = datetime.datetime(*launchtime)
    countdown_time_delta = launchdatetime-now

    print(str(countdown_time_delta) + " Until Launch!")
    days=str(countdown_time_delta.days) + " day"
    days+="s" if days != 0 else ""
    seconds = countdown_time_delta.seconds
    hours=str(int(seconds/3600)) + " hour"
    seconds-=int(seconds/3600)*3600
    hours+="s" if hours != 0 else ""
    minutes=str(int(seconds/60)) + " minute"
    seconds-=int(seconds/60)*60
    minutes+="s" if minutes != 0 else ""
    seconds=str(seconds) + " second"
    seconds+="s" if seconds != 0 else ""
    ret_string="{0}, {1}, {2}, and {3}".format(days,hours,minutes,seconds)
    return ret_string

@app.route('/launchdetails')
def launchdetails():

    launchpadDict = {}
    payloadDict = {}

    FALCON1 = "5e9d0d95eda69955f709d1eb"
    FALCON9 = "5e9d0d95eda69973a809d1ec"
    FALCONHEAVY = "5e9d0d95eda69974db09d1ed"
    STARSHIP = "5e9d0d96eda699382d09d1ee"

    Latest = requests.get("https://api.spacexdata.com/v4/launches/latest").text
    json_Latest=json.loads(Latest)

    Upcoming = requests.get("https://api.spacexdata.com/v4/launches/upcoming").text
    json_Upcoming=json.loads(Upcoming)


    #This one you should work on Kira
    #Just copy and paste the link: https://api.spacexdata.com/v4/rockets
    Rockets = requests.get("https://api.spacexdata.com/v4/rockets").text
    json_Rockets=json.loads(Rockets)

    launchpads = requests.get("https://api.spacexdata.com/v4/launchpads").text
    json_launchpads=json.loads(launchpads)

    Payload = requests.get("https://api.spacexdata.com/v4/rockets").text
    json_Payload = json.loads(Payload)

    #Copy and paste 1 of the for statements below and replace payload with a name of your choosing like rockets or something
    #then replace json_payload with json_Rockets
    #then find what name of the hash value is assigned to in the link you copied and pasted above.
    # then set that equal to what it is described as in the https://api.spacexdata.com/v4/launches/latest
    #finally print it just like the other ones below!

    for launchpad in json_launchpads:
        launchpadDict[launchpad["id"]] = launchpad["full_name"]

    for payload in json_Payload:
        payloadDict[payload["id"]] = payload["name"]

    print (payloadDict[json_Upcoming[0]["payloads"][0]])
    print (launchpadDict[json_Upcoming[0]["launchpad"]])

    details_string = "Payload: " + payloadDict[json_Upcoming[0]["payloads"][0]] + "<br>" + "LaunchPad: "  + launchpadDict[json_Upcoming[0]["launchpad"]]


    #details_string = "Mission Name: " + str(json_Latest["name"]) + "<br>" + "Launch Site: " + str(json_Latest["launchpad"]) + "<br>" + "Launch Vechicle: " + str(json_Latest["rocket"]) + "<br>" + " Payload: " + str(json_Latest["payloads"]) + "Payloads Name: "

    #+ "<br>" + " Launch Site: " + str(json_Latest["launchpads"]["full_name"]) + "<br>" + " Launch Vechicle: " + str(json_Latest["rockets"]["rocket_name"]) + "<br>" + " Payload: " + str(json_Latest["rocket"]["second_stage"]["payloads"][0]["payload_type"]) + "<br>" + "Payload Name: " + str(json_Latest["rocket"]["second_stage"]["payloads"][0]["payload_id"] + "<br>" + "Mass: " + str(json_Latest["rocket"]["second_stage"]["payloads"][0]["payload_mass_kg"]) + "kg" + "<br>" + "Manufacturer: " +  str(json_Latest["rocket"]["second_stage"]["payloads"][0]["manufacturer"])+ "<br>" + "Orbit: " + str(json_Latest["rocket"]["second_stage"]["payloads"][0]["orbit"]))

    #details_string = "Mission Name: " + str(json_Latest["name"]) + "<br>" + str(json_Latest["latest"])

    return details_string



@app.route('/upcominglaunches')
def upcominglaunches():

    Upcoming = requests.get("https://api.spacexdata.com/v3/launches/upcoming").text
    json_Upcoming=json.loads(Upcoming)

    upcoming_string = "Mission Name: " + str(json_Upcoming[0]["mission_name"]) + "\n" + " Rocket Model: " + str(json_Upcoming[0]["rocket"]["rocket_name"])
    return upcoming_string
app.run(threaded=True,port=int(os.environ.get('PORT', 5000)))
