#!/usr/bin/python

from flask import Flask, request
from flask import json
import os
import time, requests, httplib, urllib
import gmail
import time
import threading
import random

app = Flask(__name__)

_GROUPME_URL = 'api.groupme.com'
MARCSMEN_GROUP = ""
botgroup  = ""
marcsmen_token = ""
botgroup_token = ""
_GOOGLE_EVENTS_URL = ""
count = -1
beers = [
  "http://organicxbenefits.com/wp-content/uploads/2011/11/organic-beer-health-benefits.jpg",
  "http://www.beer100.com/images/beermug.jpg",
  "http://www.bristolvantage.com/wp-content/uploads/2012/02/beer-calories1.jpg",
  "http://cdn.biruwananbai.com/wp-content/uploads/2012/04/more_beer-01.jpg",
  "http://blog.collegebars.net/uploads/10-beers-you-must-drink-this-summer/10-beers-you-must-drink-this-summer-sam-adams-summer-ale.jpg",
  "http://media.treehugger.com/assets/images/2011/10/save-the-beers.jpg",
  "http://poemsforkush.files.wordpress.com/2012/04/beer.jpg",
  "http://www.wirtzbeveragegroup.com/wirtzbeveragenevada/wp-content/uploads/2010/06/Beer.jpg",
  "http://www.walyou.com/blog/wp-content/uploads/2010/06/giant-beer-glass-fathers-day-beer-gadgets-2010.jpg",
  "http://images.free-extras.com/pics/f/free_beer-911.jpg",
  "http://images.seroundtable.com/android-beer-dispenser-1335181876.jpg",
  "http://www.mediabistro.com/fishbowlDC/files/original/beer-will-change-the-world.jpg",
  "http://www.gqindia.com/sites/default/files/imagecache/article-inner-image-341-354/article/slideshow/1289/beer.JPG",
  "http://www.gqindia.com/sites/default/files/imagecache/article-inner-image-341-354/article/slideshow/1289/beer2.jpg",
  "http://www.gqindia.com/sites/default/files/imagecache/article-inner-image-341-354/article/slideshow/1289/Beer3.jpg"
]
snacks = [
  "Om nom nom!",
  "Thanks! I'll brb",
  "Omg, I was starving! THANK YOU!!",
  "Give me a break, give me a break, break me off a piece of that KitKat bar!",
  "Once you pop, you can't stop!",
  "Two for me! None for you.",
  "COOKIE! COOKIE COOKIE COOKIE COOKIE COOKIE COOKIE COOKIE COOKIE COOKIE COOKIE COOKIE COOKIE COOKIE COOKIE COOKIE COOKIE COOKIE COOKIE COOKIE COOKIE"
]

username = "_@gmail.com"
password = "*******"
toDie = False

@app.route('/groupme/ping', methods=["POST"])
def ping():
    if toDie == True:
	print "BARBERBOT PING DIEING"
	os.system("ps -ef | grep barber | grep -v grep | tr -s ' ' | cut -d' ' -f2 | xargs kill -9")
    if request.headers['Content-Type'] == 'application/json':
        data = request.get_json();
        #grab the last message
        if "barberbot" in data['text'].lower():
            if "events" in data['text']:
                r = requests.get(_GOOGLE_EVENTS_URL)
                data = r.json()
                events = data['items']

                text2send = "The next 3 upcoming events are:\n"
                for event in events:
                    theDate = event['start']

                    if 'dateTime' in theDate.keys():
                        iso_time = theDate['dateTime']
                        tuple_time = time.strptime(iso_time, "%Y-%m-%dT%H:%M:%S-06:00")
                        iso_time = time.strftime("%A, %m-%d-%Y at %I:%M %p", tuple_time)
                    else:
                        iso_time = theDate['date']
                        tuple_time = time.strptime(iso_time, "%Y-%m-%d")
                        iso_time = time.strftime("%A, %m-%d-%Y", tuple_time)
                    text2send = text2send + " " + event['summary'] + " on " + iso_time + "\n"

            elif "Thomas" in data['name'] and MARCSMEN_GROUP in data['group_id']:
                return ""
            elif "beer" in data['text']:
                text2send = random.choice(beers)
            elif "weather" in data['text']:
                text2send = "It is very cold outside."
            elif "twerk" in data['text']:
                text2send = "*twerking like Miley Cirus*"
            elif "Miley" in data['text']:
                text2send = "I came in like a wrecking ball!"
            elif "snack" in data['text'] or "treat" in data['text'] or "cookie" in data['text']:
                text2send = random.choice(snacks)
            elif "sing" in data['text']:
                text2send = "la la la la la"
            elif ( "Cory" in data['name'] or "Chris" in data['name'] ) and "herpderp" in data['text']:
		text2send = "Sorry to ruin the fun.. I'll leave now :("
                os.system("ps -ef | grep barber | grep -v grep | tr -s ' ' | cut -d' ' -f2 | xargs kill -9")
            else:
                if botgroup in data['group_id']:
                    text2send = "I don't understand that command"
                else:
                    return ""

            conn = httplib.HTTPSConnection(_GROUPME_URL)
            headers = {"Content-type": "application/x-www-form-urlencoded"}
            if botgroup in data['group_id']:
                params = urllib.urlencode({'text': text2send, 'bot_id': botgroup_token})
                print "true"
            else:
                params = urllib.urlencode({'text': text2send, 'bot_id': marcsmen_token})
            conn.request("POST", "/v3/bots/post", params, headers)
            response = conn.getresponse()
            print response.status, response.reason, response.getheaders()
            conn.close()
            return text2send

        elif " bot " in data['text']:
            text2send = "If you have something to say about me, address it to me directly punk. =.="

            conn = httplib.HTTPSConnection(_GROUPME_URL)
            headers = {"Content-type": "application/x-www-form-urlencoded"}
            if botgroup in data['group_id']:
                params = urllib.urlencode({'text': text2send, 'bot_id': botgroup_token})
                print "true"
            else:
                params = urllib.urlencode({'text': text2send, 'bot_id': marcsmen_token})
            conn.request("POST", "/v3/bots/post", params, headers)
            response = conn.getresponse()
            print response.status, response.reason, response.getheaders()
            conn.close()
            return text2send
        return ""
def checkGmail():
    print("Started checkGmail")
    while True:
	print "toDie - " + str(toDie)
	if toDie:
            print "BARBERBOT CHECK GMAIL DIEING"
            os.system("ps -ef | grep barber | grep -v grep | tr -s ' ' | cut -d' ' -f2 | xargs kill -9")
        try:
            g = gmail.login(username, password)
            if not g:
		pass
            emails = g.inbox().mail(to="email@site.com", unread=True, prefetch=True)
        except:
            print "Login failed.."
            pass
	#emails = g.inbox().mail(to="email@site.com", unread=True, prefetch=True)
	if len(emails) > 0:
            for email in emails:
		sender = " ".join(email.fr.split()[:2])
		subject = email.subject
		email.read()
		print "Attention! New Member email from %s - %s" % (sender, subject)
		text2send = "Attention! New Member email from %s - %s" % (sender, subject)
		conn = httplib.HTTPSConnection(_GROUPME_URL)
		headers = {"Content-type": "application/x-www-form-urlencoded"}
		params = urllib.urlencode({'text': text2send, 'bot_id': marcsmen_token})
		#params = urllib.urlencode({'text': text2send, 'bot_id': botgroup_token})
		conn.request("POST", "/v3/bots/post", params, headers)
		response = conn.getresponse()
		print response.status, response.reason, response.getheaders()
		conn.close()
	time.sleep(600)

def runApp():
    print("Started runApp")
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    threads = []
    t = threading.Thread(target = runApp)
    t.start()
    time.sleep(2)
    t = threading.Thread(target = checkGmail)
    t.start()


#@app.route('/messages', methods = ['POST'])
#def api_message():
#
#    if request.headers['Content-Type'] == 'text/plain':
#        return "Text Message: " + request.data
#
#    elif request.headers['Content-Type'] == 'application/json':
#        return "JSON Message: " + json.dumps(request.json)
#
#    elif request.headers['Content-Type'] == 'application/octet-stream':
#        f = open('./binary', 'wb')
#        f.write(request.data)
#        f.close()
#        return "Binary message written!"
#
#    else:
#        return "415 Unsupported Media Type ;)"


#curl -d '{"text" : "This is a test for the bot that Chris is working on", "bot_id" : ""}' https://api.groupme.com/v3/bots/post

#text2send = "You will do nothing =.="
#conn = httplib.HTTPSConnection(_GROUPME_URL)
#conn.set_debuglevel(3)
#headers = {"Content-type": "application/x-www-form-urlencoded"}
#params = urllib.urlencode({'text': text2send, 'bot_id': marcsmen_token})
#conn.request("POST", "/v3/bots/post", params, headers)
#response = conn.getresponse()
#print response.status, response.reason, response.getheaders()
#conn.close()
