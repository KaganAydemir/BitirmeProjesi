from flask import Flask, render_template, Response, request, flash
from flask_socketio import SocketIO
from ultralytics import YOLO
import cv2


from core_service.stream import Stream
from core_service.object_counter import Counter
from core_service.detector import Detector
from core_service.motor import Motor
# initialize flask & socketio
app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwerty123'

socketio = SocketIO()
socketio.init_app(app)

@app.route("/")
def index():
    camera = request.args.get("camera")
    mode_req = request.args.get("mode")

    if camera is not None and camera == 'off' and stream.status() == True:
        stream.close()
        flash("Konveyör durduruldu!", "info")
    elif camera is not None and camera == 'on' and stream.status() == False:
        counter.counter_mode = mode_req
        detector.counter = counter
        stream.counter = counter
        stream.open()
        flash("Konveyör başlatıldı!", "success")

    setting = dict(
        stream_on = stream.status(),
        w = w,
        mode = ['area', 'line', 'multiline'],
        selected_mode = mode_req
    )
    return render_template("index.html", setting = setting)

@app.route('/video_feed')
def video_feed():
    return Response(stream.gen_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')
#
@app.route("/model")
def model():
    return render_template("model.html")

@app.route("/setting")
def setting():
    return render_template("setting.html")
    
@socketio.on('reset_counter')
def handle_reset_counter(msg):
    print('received :', msg)
    counter.set_null_counter()

if __name__ == '__main__':
    global detector, mot
    w, h = 480, 320

    model = YOLO("yolov8n.pt")
    classes = model.names
    classes.update({80:'total'})
    classes.update({81:'unidentified'})
    classes.update({47:'orange'})        
    # initialize counter object
    lines = []
    lines.append([int(w*0.20), 0, int(w*0.20), h]) # LINE 0, x0, y0, x1, y1
    #lines.append([int(w*0.80), 0, int(w*0.80), h]) # LINE 1, x0, y0, x1, y1
    counter = Counter(classes, mode='line', lines=lines, threshDist = 30) #  mode='line', 'area', 'multiline'

    # initialize model
    detector = Detector(counter, socketio, classes)
    mot = Motor()
    detector.load_model("yolov8n.pt")
    # initialize stream object
    cam = cv2.VideoCapture(0)
    stream = Stream(cam, detector, counter, mot, socketio, classes)

    # initialize background task
    #socketio.start_background_task(target=detector.main)
    socketio.start_background_task(target=mot.main)
    # run flask-socketio
    socketio.run(app, host="0.0.0.0")
    stream.close()
