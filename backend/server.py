from concurrent.futures import process
from sys import flags
from threading import Thread
from flask import Flask
from flask_threaded_sockets import Sockets, ThreadedWebsocketServer
import handtracker
import io
import cv2
import numpy as np
import base64
import threading
import sys

IP = "0.0.0.0"

if (len(sys.argv) >= 2):
    PORT = sys.argv[1]
else:
    PORT = 2052

app = Flask(__name__)
sockets = Sockets(app)

@sockets.route("/detect")
def detect(ws):

    currentData = ""

    while (not ws.closed):
        rawFrame = ws.receive()
        
        processFrame(rawFrame, ws)

def processFrameInThread(data, ws):
    t = threading.Thread(target=processFrame, args=(data, ws,))
    t.start()

def processFrame(frameData, ws):
    splitData = frameData.split(",")
    scrapedData = [splitData[i:i + 3] for i in range(0, len(splitData), 3)] # Split data into chunks of 3

    label, perc = handtracker.predictData(scrapedData)

    print(label)
    

srv = ThreadedWebsocketServer(IP, PORT, app)
srv.serve_forever()