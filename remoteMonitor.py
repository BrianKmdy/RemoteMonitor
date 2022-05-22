import flask
import threading
import imageRecorder
import time
import websockets
import asyncio

app = flask.Flask(__name__)

def broadcastThread():
    i = 0
    while True:
        image = imageRecorder.imageQueue.get()
        # socketio.emit('frame', {'index': i, 'bytes': image})
        i += 1
        time.sleep(1)

async def hello(websocket, path):
    for message in websocket:
        print(message)

    for i in range(100):
        print('Sending hello')
        await websocket.send('hello {}'.format(i))
        time.sleep(1)

def websocketThread():
    asyncio.set_event_loop(asyncio.new_event_loop())
    start_server = websockets.serve(hello, '0.0.0.0', 5001)
    asyncio.get_event_loop().run_until_complete(start_server)

@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/capture')
def capture():
    if not imageRecorder.imageQueue.empty():
        print(imageRecorder.imageQueue.qsize())
        return flask.Response(imageRecorder.imageQueue.get(), mimetype="image/jpg")
    return flask.Response()

if __name__ == '__main__':
    # threading.Thread(target=imageRecorder.capture, daemon=True).start()
    threading.Thread(target=broadcastThread, daemon=True).start()
    threading.Thread(target=websocketThread, daemon=True).start()
    

    app.run(host='0.0.0.0')
