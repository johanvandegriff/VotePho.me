#!/usr/bin/python3
from flask import Flask, request, render_template, url_for
import json, os, random
from PIL import Image

TITLE = "VotePho.me - Vote for a Photo" #site title, used in the title bar and the heading within the page

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024    # 100 Mb limit

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

VOTES_FILE="static/images/votes.json"

def saveVotesFile(vote_data):
    json.dump(vote_data, open(VOTES_FILE, 'w'), indent=2)

def loadVotesFile():
    try:
        vote_data = json.load(open(VOTES_FILE, 'r'))
    except FileNotFoundError:
        # if the file doesn't exist, create it with an empty list
        vote_data = {'raw_votes':{}, 'tally':{}, 'titles':{}, 'captions':{}}
        saveVotesFile(vote_data)
    return vote_data

def isValidImage(image):
    ext = os.path.splitext(image)[1]
    return ext in (".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG")

def getImages():
    images = os.listdir("static/images")
    #keep only the image files
    images = [image for image in images if isValidImage(image)]
    return images

#the index.html page, which the user sees
@app.route('/')
def index():
    return render_template("index.html", title=TITLE)

@app.route('/vote')
def vote():
    # ip = request.remote_addr #the ip address of the user. this will prevent duplicate votes
    id =  request.args['id'] #random number generated and stored as a cookie
    img = request.args['img']
    vote_data = loadVotesFile()
    alreadyVoted = id in vote_data['raw_votes']
    sameVote = alreadyVoted and vote_data['raw_votes'][id] == img
    if sameVote:
        return "You already voted for this photo!"

    vote_data['raw_votes'][id] = img
    vote_data['tally'] = {}
    for img in getImages():
        vote_data['tally'][img] = 0

    for id,img in vote_data['raw_votes'].items():
        img = os.path.basename(img)
        if not img in vote_data['tally']:
            vote_data['tally'][img] = 0
        vote_data['tally'][img] += 1
    saveVotesFile(vote_data)
    #doesn't render a page, just pops up a message
    if alreadyVoted:
        return "Your vote has been changed!"
    else:
        return "Thanks for voting! To change your vote, simply vote for a different image."

@app.route('/votes')
def votes():
    return loadVotesFile()['tally']

#the json data, which the script reads (not meant for the user)
@app.route('/gallery_json')
def gallery_json():
    images = getImages() #get a list of all the images in the directory
    # random.shuffle(images) #shuffle the images to help eliminate bias

    vote_data = loadVotesFile()
    titles = vote_data['titles']
    captions = vote_data['captions']
    tally = vote_data['tally']

    #convert the list to a JSON format that the JS will use
    images_json = []
    for i, img in enumerate(images):
        item = {"id": i+1, "url":"images/"+img}
        if img in titles:
            item['title'] = titles[img]
        if img in captions:
            item['caption'] = captions[img]
        if img in tally:
            item['tally'] = tally[img]
        images_json.append(item)
    
    data = {"album": {"name": TITLE}, "photos": images_json}
    return json.dumps(data)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    target = os.path.join(APP_ROOT, 'static/images/')

    if "clear" in request.form and request.form["clear"] == "yes":
        for image in getImages():
            os.remove("static/images/"+image)
        os.remove("static/images/votes.json")

    if "remove" in request.form and request.form["remove"] == "yes":
        image = request.form["img"]
        os.remove("static/images/"+image)

    if "rotate" in request.form and request.form["rotate"] == "yes":
        image = request.form["img"]
        # os.remove("static/images/"+image)


    # create image directory if not found
    if not os.path.isdir(target):
        os.mkdir(target)

    message = ""
    print(request.files)
    print(len(request.files))
    if len(request.files) > 0:
        upload = request.files.getlist("file")[0]
        print("File name: {}".format(upload.filename))
        filename = upload.filename.replace("'","") #filter out '

        # file support verification
        ext = os.path.splitext(filename)[1]
        if ext in (".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"):
            # save file
            destination = "/".join([target, filename])
            print("File saved to to:", destination)
            upload.save(destination)

            #save title and caption if given
            vote_data = loadVotesFile()
            write = False
            if 'title' in request.form:
                vote_data['titles'][filename] = request.form['title']
                write = True
            if 'caption' in request.form:
                vote_data['captions'][filename] = request.form['caption']
                write = True
            if write:
                saveVotesFile(vote_data)

            message = "File uploaded"
        else:
            message = "File type not supported, please use .png, .jpg, or .jpeg"
    return render_template("admin.html", message=message, images=getImages(), votes=loadVotesFile()['tally'])

if __name__ == "__main__":
    app.run()
