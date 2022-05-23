import imageRecorder
import humidityReader
import threading
import time
import os
import datetime
import yagmail
import yaml

def getCaptureName():
    return datetime.datetime.now().strftime("%a, %b %d %H:%M:%S")

def saveCaptures():
    global period
    frameIndex = 0
    currentPeriod = 0

    with open("email.yaml", "r") as f:
        email = yaml.safe_load(f)

    while True:
        if len(imageRecorder.imageQueue) > 0:
            image = imageRecorder.imageQueue.popleft()
            if imageRecorder.getStartOfPeriod() != currentPeriod:
                currentPeriod = imageRecorder.getStartOfPeriod()
                captureName = getCaptureName()
                image.name = '{}.jpg'.format(captureName)

                print('Sending image {}'.format(captureName))
                yag = yagmail.SMTP({email['from']: email['fromName']}, oauth2_file='auth.json')
                yag.send(to=email['to'], subject=captureName, attachments=image)

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