import cv2


class Stream():
    def __init__(self, camera_src, detector, counter, mot, socketio, classes):
        self.camera_src = camera_src
        self.camera = None
        self.prev_messages = ""
        self.socketio = socketio
        self.detector = detector
        self.counter = counter
        self.mot = mot
        self.classes = classes

    def gen_frames(self):
        self.prev_messages = ""
        while True:
            if self.camera is not None:
                ret, frame = self.camera.read()
                if not ret:
                    break
                self.mot.detection_complete = False
                if not self.mot.is_running:
                    frame = self.detector.detect_object(ret, frame)
                    messages = []
                    print("detection yapiliyo") 
                    # frame = self.counter.draw_line(frame)
                    for counter_object in self.counter.counter_objects:
                        msg = {}
                        for key in counter_object:
                            #print(key)
                            if counter_object[key]['counter'] > 0:
                                msg[self.classes[key]] = counter_object[key]['counter']
                                #print(self.classes[key])
                                print(msg[self.classes[key]])
                        messages.append(msg)
                    if len(messages) > 0:
                        # trigger buzzer & send counter to browser
                        if messages != self.prev_messages:
                            self.prev_messages = messages
                            self.socketio.emit("counter_event", {
                                "type": 'line',
                                "messages": messages
                            })
                    self.mot.detection_complete = True
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                if frame is None:
                    continue
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def close(self):
        if self.camera is not None:
            self.camera.release()
            self.camera = None

    def open(self):
        self.camera = self.camera_src

    def status(self):
        return self.camera is not None
