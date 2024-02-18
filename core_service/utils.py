import os
import cv2 
import numpy as np 

class Utils():
    def draw_ped(self, img, label, x0, y0, xt, yt, font_size=0.4, color=(255, 127, 0), text_color=(255, 255, 255)):

        y0, yt = max(y0 - 15, 0), min(yt + 15, img.shape[0])
        x0, xt = max(x0 - 15, 0), min(xt + 15, img.shape[1])

        (w, h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_size, 1)
        cv2.rectangle(img,
                      (x0, y0 + baseline),
                      (max(xt, x0 + w), yt),
                      color,
                      2)
        cv2.rectangle(img,
                      (x0, y0 - h - baseline),
                      (x0 + w, y0 + baseline),
                      color,
                      -1)
        cv2.rectangle(img,
                      (x0, y0 - h - baseline),
                      (x0 + w, y0 + baseline),
                      color,
                      2)
        cv2.putText(img,
                    label,
                    (x0, y0),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_size,
                    text_color,
                    1,
                    cv2.LINE_AA)
        return img
    def postprocess(self,results, frame):
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
                   "teddy bear", "hair drier", "toothbrush"
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
                classIds.append(cls)
                print("Class name -->", classes[cls])
                # object details
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2

                cv2.putText(frame, classes[cls], org, font, fontScale, color, thickness)
        return frame

