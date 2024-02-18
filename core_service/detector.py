import cv2
from ultralytics import YOLO
import numpy as np
import time
class Detector():
    def __init__(self, counter, socketio, classes):
        self.classes = classes
        self.color_maps = {}
        self.net = None
        self.layerOutput = []

        self.output = []
        self.frame = []
        self.ret = []

        self.target_w = 244
        self.target_h = 244

        self.counter = counter
        self.socketio = socketio

    def load_model(self, model="yolov8n.pt"):
        # load pretrained model
        self.net = YOLO(model)

    def main(self):
        while True :
            if self.ret:
                start = time.time()
                self.output = self.net.predict(self.frame)
                end = time.time()
                t = end-start
                inf = '%.2f' % (t)
                self.socketio.emit("inference_event", inf)

    def detect_object(self, ret, frame):
        self.frame = frame
        self.ret = ret
        if self.output:
            return self.counter.postprocess(self.output, frame)
        else :
            return frame