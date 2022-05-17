import flask
import flask_socketio
import threading
import imageRecorder
import time

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

lastAck = 0
bufferSeconds = 1
frameIndex = 0

def broadcastThread():
    global lastAck
    global bufferSeconds
    global frameIndex
    while True:
        print('Comparison: {} and {}'.format(frameIndex - lastAck, bufferSeconds * imageRecorder.frameRate))
        if len(imageRecorder.imageQueue) > 0 and frameIndex - lastAck < bufferSeconds * imageRecorder.frameRate:
            image = imageRecorder.imageQueue.popleft()
            print('Sending frame {}'.format(frameIndex))
            socketio.emit('frame', {'num': frameIndex, 'bytes': image})
            frameIndex += 1
        else:
            time.sleep(0.1)

@app.route('/')
def home():
    return flask.render_template('index.html')

@socketio.on('connect')
def connect(auth):
    print('User connected')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@socketio.on('ack')
def handle_json(json):
    global lastAck
    print('Received ack ' + str(json))
    lastAck = json['num']

if __name__ == '__main__':
    threading.Thread(target=imageRecorder.capture, daemon=True).start()
    threading.Thread(target=broadcastThread, daemon=True).start()
    socketio.run(app, host='0.0.0.0')
    # app.run(host='0.0.0.0')
