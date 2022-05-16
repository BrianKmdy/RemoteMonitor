import flask
import sqlite3
import json
import imageRecorder
import threading

app = flask.Flask(__name__)

@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/data')
def data():
    con = sqlite3.connect('humidity.db')
    response = json.dumps([row for row in con.cursor().execute('SELECT * from humidity')])
    con.close()
    return response

@app.route('/capture')
def capture():
    if not imageRecorder.imageQueue.empty():
        print(imageRecorder.imageQueue.qsize())
        return flask.Response(imageRecorder.imageQueue.get(), mimetype="image/jpg")
    return flask.Response()

if __name__ == '__main__':
    threading.Thread(target=imageRecorder.capture, daemon=True).start()
    app.run(host='0.0.0.0')