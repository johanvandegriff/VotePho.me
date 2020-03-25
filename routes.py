#!/usr/bin/python3
from flask import Flask, request, render_template, url_for

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html", text="Hello, World!")

if __name__ == "__main__":
    app.run()
