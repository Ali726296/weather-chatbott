from flask import Flask, render_template
import os

template_dir = os.path.join(os.path.dirname(__file__), "../templates")

app = Flask(__name__, template_folder=template_dir)

@app.route("/")
def home():
    return render_template("index.html")

handler = app
