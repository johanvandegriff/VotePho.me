#!/usr/bin/python3
from flask import Flask, request, render_template, url_for
import json, os, random

TITLE = "VotePho.me - Vote for a Photo" #site title, used in the title bar and the heading within the page

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#the index.html page, which the user sees
@app.route('/')
def index():
    return render_template("index.html", title=TITLE)

#the json data, which the script reads (not meant for the user)
@app.route('/gallery_json')
def gallery_json():
    images = os.listdir("static/images") #get a list of all the images in the directory
    random.shuffle(images) #shuffle the images to help eliminate bias

    #convert the list to a JSON format that the JS will use
    images_json = [{"id": i+1, "url":"images/"+img} for i,img in enumerate(images)]
    data = {"album": {"name": TITLE}, "photos": images_json}
    return json.dumps(data)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    target = os.path.join(APP_ROOT, 'static/images/')

    if 'clear' in request.form:
        for image in os.listdir("static/images"):
            os.remove("static/images/"+image)


    # create image directory if not found
    if not os.path.isdir(target):
        os.mkdir(target)

    message = ""
    print(request.files)
    print(len(request.files))
    if len(request.files) > 0:
        upload = request.files.getlist("file")[0]
        print("File name: {}".format(upload.filename))
        filename = upload.filename

        # file support verification
        ext = os.path.splitext(filename)[1]
        if ext in (".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"):
            message = "File uploaded"
        else:
            message = "File type not supported, please use .png, .jpg, or .jpeg"

        # save file
        destination = "/".join([target, filename])
        print("File saved to to:", destination)
        upload.save(destination)


    return render_template("admin.html", message=message, images=os.listdir("static/images"))

if __name__ == "__main__":
    app.run()
