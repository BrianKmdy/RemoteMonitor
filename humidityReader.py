import sqlite3
import Adafruit_DHT
import time
import traceback

DHT_MODEL = 22
DHT_PIN = 4

humidity = 0
temperature = 0

def getHumidityData():
    global humidity
    global temperature

    try:
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(DHT_MODEL, DHT_PIN)
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        traceback.print_exc(e)