#!/usr/bin/python3
from flask import Flask, request, render_template, url_for
import json, os, random

TITLE = "VotePho.me" #site title, used in the title bar and the heading within the page

app = Flask(__name__)

#the index.html page, which the user sees
@app.route('/')
def index():
    return render_template('index.html', title=TITLE)

#the json data, which the script reads (not meant for the user)
@app.route('/gallery_json')
def gallery_json():
    images = os.listdir("static/images") #get a list of all the images in the directory
    random.shuffle(images) #shuffle the images to help eliminate bias

    #convert the list to a JSON format that the JS will use
    images_json = [{"id": i+1, "url":"images/"+img} for i,img in enumerate(images)]
    data = {"album": {"name": TITLE}, "photos": images_json}
    return json.dumps(data)

if __name__ == "__main__":
    app.run()
