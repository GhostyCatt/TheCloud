from flask import Flask, render_template
from threading import Thread

App = Flask('')

@App.route('/')
def home():
    return render_template(
        "Index.html"
    )

def run():
  App.run(
        host = '0.0.0.0',
        port = 5000
    )

def Start():
    thread = Thread(target = run)
    thread.start()