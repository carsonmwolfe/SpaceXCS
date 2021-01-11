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
    RocketDict = {}

    Latest = requests.get("https://api.spacexdata.com/v4/launches/latest").text
    json_Latest=json.loads(Latest)

    Upcoming = requests.get("https://api.spacexdata.com/v4/launches/upcoming").text
    json_Upcoming=json.loads(Upcoming)

    Rockets = requests.get("https://api.spacexdata.com/v4/rockets").text
    json_Rockets=json.loads(Rockets)

    launchpads = requests.get("https://api.spacexdata.com/v4/launchpads").text
    json_launchpads=json.loads(launchpads)

    Payload = requests.get("https://api.spacexdata.com/v4/payloads").text
    json_Payload = json.loads(Payload)


    for launchpad in json_launchpads:
        launchpadDict[launchpad["id"]] = launchpad["full_name"]

    for payload in json_Payload:
        payloadDict[payload["id"]] = payload["name"]

    for rockets in json_Rockets:
        RocketDict[rockets["id"]] = rockets["name"]


    print (payloadDict[json_Upcoming[0]["payloads"][0]])
    print (RocketDict[json_Upcoming[0]["rocket"]])
    print (launchpadDict[json_Upcoming[0]["launchpad"]])


    details_string = "Mission Name: " + str(json_Upcoming[0]["name"]) + "<br>" + "Launch Time: " + str(json_Upcoming[0]["date_local"]) + " Local Time" + "<br>" +"---------------Payload Detials----------------------" + "<br>" +"Payload: " + payloadDict[json_Upcoming[0]["payloads"][0]] + "<br>" + "Payload Mass: " + str(json_Payload[0]["mass_kg"]) + "kg" + "<br>" + "Payload Orbit: " + str(json_Payload[0]["orbit"]) + "<br>" + "----------------------------------------------------" + "<br>" + "LaunchPad: "  + launchpadDict[json_Upcoming[0]["launchpad"]] + "<br>" + "Launch Vechicle: " + RocketDict[json_Upcoming[0]["rocket"]] + "<br>" + "Launch Details: " + str(json_Upcoming[0]["details"]) + "<br>" + "Mission Patch: " + str(json_Upcoming[0]["links"]["patch"]["large"])


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
app.run(host="0.0.0.0",threaded=True,port=int(os.environ.get('PORT', 5000)))
