from flask import Flask
from threading import Thread

App = Flask('')

@App.route('/')
def home():
    return "Bot has connected to discord!"

def run():
  App.run(
        host = '0.0.0.0',
        port = 6666
    )

def Start():
    thread = Thread(target = run)
    thread.start()