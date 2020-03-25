#!/usr/bin/python3
from flask import Flask, request, render_template, url_for
import json, os

app = Flask(__name__)
# gallery_JSON = open("gallery_images.json").read()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gallery_json')
def gallery_json():
    images = os.listdir("static/images")
    images_json = [{"id": i+1, "url":"images/"+img} for i,img in enumerate(images)]
    data = {
        "album": {
            "name": "VotePho.me"
        },
        "photos": images_json
    }
    # print(json.dumps(data, indent=4))
    return json.dumps(data)
    # return json.dumps(gallery_JSON)

if __name__ == "__main__":
    app.run()
