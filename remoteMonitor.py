import flask
import flask_socketio
import threading
import imageRecorder

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

i = 0
def broadcastThread():
    global i
    while True:
        image = imageRecorder.imageQueue.get()
        print('Sending image ' + str(i))
        socketio.emit('frame', {'index': i, 'bytes': image})
        i += 1

@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/capture')
def capture():
    if not imageRecorder.imageQueue.empty():
        print(imageRecorder.imageQueue.qsize())
        return flask.Response(imageRecorder.imageQueue.get(), mimetype="image/jpg")
    return flask.Response()

@socketio.on('connect')
def connect(auth):
    print('User connected')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    threading.Thread(target=imageRecorder.capture, daemon=True).start()
    threading.Thread(target=broadcastThread, daemon=True).start()
    socketio.run(app, host='0.0.0.0')
    # app.run(host='0.0.0.0')