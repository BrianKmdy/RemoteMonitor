import humidityReader
from io import BytesIO
import time
import datetime
from picamera import PiCamera
import collections

frameCount = 0
bufferSeconds = 10
period = 15 # Length of period in seconds

maxQueueSize = 10
imageQueue = collections.deque(maxlen=maxQueueSize)

def getOverlayText():
    return "{}\nTemp: {:.1f}C  Humidity: {:.1f}%".format(
        datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        humidityReader.temperature,
        humidityReader.humidity)
        
def getStartOfPeriod():
    global period
    return int(time.time() / period) * period

def capture():
    print('Capture thread started')

    global imageQueue
    global frameRate
    global frameCount
    global maxQueueSize

    # Create the in-memory stream
    camera = PiCamera()
    imageBytes = BytesIO()
    camera.vflip = True
    camera.resolution = (1440, 1080)
    camera.annotate_text_size = 20
    camera.annotate_text = getOverlayText()
    camera.start_preview()
    time.sleep(2)

    try:
        start = time.time()
        for frame in camera.capture_continuous(imageBytes, 'jpeg', burst=True, quality=35):
            print('Captured image {} in time {:.2f}s'.format(frameCount, time.time() - start))
            imageQueue.append(imageBytes.getvalue())

            frameCount += 1
            imageBytes.seek(0)
            imageBytes.truncate()

            time.sleep(getStartOfPeriod() + period - time.time())
            camera.annotate_text = getOverlayText()
            start = time.time()
    except KeyboardInterrupt:
        pass
