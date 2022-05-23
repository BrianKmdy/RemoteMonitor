import imageRecorder
import humidityReader
import threading
import time
import os
import datetime

captureDirectory = '/home/pi/captures'

def getCaptureName():
    return datetime.datetime.now().strftime("%Y-%m-%d/%H/%Y-%m-%d_%H:%M:%S.jpg")

def saveCaptures():
    global period
    os.makedirs(captureDirectory, exist_ok=True)
    frameIndex = 0
    currentPeriod = 0
    while True:
        if len(imageRecorder.imageQueue) > 0:
            image = imageRecorder.imageQueue.popleft()
            if imageRecorder.getStartOfPeriod() != currentPeriod:
                currentPeriod = imageRecorder.getStartOfPeriod()
                capturePath = os.path.join(captureDirectory, getCaptureName())
                print('Saving image {}'.format(capturePath))
                if not os.path.exists(os.path.dirname(capturePath)):
                    os.makedirs(os.path.dirname(capturePath), exist_ok=True)
                with open(capturePath, 'wb') as f:
                    f.write(image)
                frameIndex += 1
        else:
            time.sleep(0.1)

if __name__ == '__main__':
    try:
        threading.Thread(target=imageRecorder.capture, daemon=True).start()
        threading.Thread(target=humidityReader.getHumidityData, daemon=True).start()
        saveCaptures()
    except KeyboardInterrupt:
        pass