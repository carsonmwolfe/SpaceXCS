# SpaceX CS Project Backend
# Last Updaed December 4th
import flask
import datetime
import requests
import json

app=flask.Flask(__name__)

@app.route('/')
#Home Page
def index():
    return flask.render_template('index.html')

@app.route('/countdown')
def countdown():

    Latest = requests.get("https://api.spacexdata.com/v3/launches/latest").text
    json_Latest=json.loads(Latest)
    Upcoming = requests.get("https://api.spacexdata.com/v3/launches/upcoming").text
    json_Upcoming=json.loads(Upcoming)
    countdowntimer = str(json_Upcoming[0]["launch_date_local"])
    now = datetime.datetime.now()
    liftoff = str(now)
    countdowntimer = str(json_Upcoming[0]["launch_date_local"])
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


    Latest = requests.get("https://api.spacexdata.com/v3/launches/latest").text
    json_Latest=json.loads(Latest)

    Upcoming = requests.get("https://api.spacexdata.com/v3/launches/upcoming").text
    json_Upcoming=json.loads(Upcoming)

    details_string = "Mission Name:" + str(json_Upcoming[0]["mission_name"] + "\n" + "Rocket Model:" + str(json_Upcoming[0]["rocket"]["rocket_name"]))
    return details_string





@app.route('/launchinformation')
def launchinformation():

@app.route('/upcominglaunches')
def upcominglaunches():


app.run(threaded=True,port=int(os.environ.get('PORT', 5000)))
