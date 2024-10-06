from flask import Flask, render_template, Response
from camera import VideoCamera
import time

app = Flask(__name__)

camera = None 

def get_camera_instance():
    global camera
    if camera is None:
        camera = VideoCamera()
    return camera

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vdo')
def vdo():
    global camera
    if camera is None:
        camera = VideoCamera()
    return render_template('video.html')

def gen(camera):
    while True:
        start_time = time.time()
        frame = camera.get_frame()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-type:image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        if time.time() - start_time >= 40:
            break

@app.route('/feed')
def feed():
    return Response(gen(get_camera_instance()),
                    mimetype='multipart/x-mixed-replace;boundary=frame')

@app.route('/count')
def final_count():
    global camera
    if camera is not None:
        camera.__del__()
        count = camera.get_count() 
        camera = None
        return render_template('count.html', count=count)
    return render_template('count.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
