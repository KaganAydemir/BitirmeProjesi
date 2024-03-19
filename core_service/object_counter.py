import cv2
import numpy as np
from .utils import Utils
import math
utils = Utils()

class Counter():
    def __init__(self, classes, mode='multiline', lines=[], threshDist = 50, direction=('left', 'right')):
        self.classes = classes
        self.frame_id = 0
        self.counter_objects = []
        self.counter_mode = mode
        self.lines = lines 
        self.threshDist = threshDist
        self.direction = direction
        self.set_null_counter()

    def set_null_counter(self):
        self.counter_objects = []
        for __ in self.lines :
            class_counter = {}
            for class_id in self.classes:
                class_counter[class_id] = {
                                            'in' : False,
                                            'frame_id' : 0,
                                            'counter' : 0     
                                            }
            self.counter_objects.append(class_counter)

    def postprocess(self, results, frame):
        self.frame_id += 1
        print("object counter postprocess")
        classIds = []
        confidences = []
        boxes = []

        classes = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                   "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                   "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
                   "umbrella",
                   "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
                   "baseball bat",
                   "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass",
                   "cup",
                   "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                   "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                   "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard",
                   "cell phone",
                   "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
                   "scissors",
                   "teddy bear", "hair drier", "toothbrush","total","unidentified"
                   ]
        for r in results:
            boxe = r.boxes

            for box in boxe:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values
                boxes.append([x1, y1, x2, y2])
                # put box in cam
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100
                confidences.append(confidence)
                print("Confidence --->", confidence)

                # class name

                cls = int(box.cls[0])
                if cls==47:
                    cls=49
                if cls==52:
                    cls=51
                if confidence < 0.45 and not cls==64 and not cls==79 and not cls==51 and not cls==0:
                    cls = 81
                if not cls==0:    
                    classIds.append(cls)
                print("Class name -->", classes[cls])
                # object details
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2
                cv2.putText(frame, classes[cls], org, font, fontScale, color, thickness)
        for i in classIds:
           
            self.counter_objects[0][i]['counter'] += 1
            self.counter_objects[0][80]['counter'] +=1
            
        return frame

    def draw_line(self, frame):
        if self.counter_mode == 'line' :
            x1, y1, x2, y2 = self.lines[0]
            frame = cv2.line(frame, (x1, y1), (x2, y2 ), (255, 0, 255), 3)
        elif self.counter_mode == 'multiline':
            for line in self.lines :
                x1, y1, x2, y2 = line
                frame = cv2.line(frame, (x1, y1), (x2, y2 ), (255, 0, 255), 3)          
        return frame
