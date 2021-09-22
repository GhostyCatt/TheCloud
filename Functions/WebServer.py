from flask import Flask
from threading import Thread

App = Flask('')

@App.route('/')
def home():
    return "Bot has connected to discord!"

def run(port:int):
  App.run(
        host = '0.0.0.0',
        port = port
    )

def Start(port:int = 6666):
    thread = Thread(target = run(port))
    thread.start()