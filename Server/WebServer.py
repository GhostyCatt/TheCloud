from flask import Flask
from threading import Thread

App = Flask('')

@App.route('/')
def home():
    return ""

def run():
  App.run(
        host = '0.0.0.0',
        port = 5000
    )

def Start():
    thread = Thread(target = run)
    thread.start()