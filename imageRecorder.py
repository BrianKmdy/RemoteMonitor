from io import BytesIO
import time
import datetime
from picamera import PiCamera
import collections
import humidityReader

frameRate = 2
frameCount = 0
bufferSeconds = 10

maxQueueSize = int(frameRate * bufferSeconds)
imageQueue = collections.deque(maxlen=maxQueueSize)

def getOverlayText():
    return "{}\n{:.1f}C   {:.1f}%".format(
        datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        humidityReader.temperature,
        humidityReader.temperature)

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
    camera.framerate = frameRate
    camera.annotate_text = getOverlayText()
    camera.start_preview()
    time.sleep(1)

    try:
        start = time.time()
        for frame in camera.capture_continuous(imageBytes, 'jpeg', burst=True, quality=50):
            print('Captured image {} in time {:.2f}s'.format(frameCount, time.time() - start))
            imageQueue.append(imageBytes.getvalue())
            print('Queue size: {}'.format(len(imageQueue)))
            print('Saved image {} in time {:.2f}s'.format(frameCount, time.time() - start))

            frameCount += 1
            start = time.time()
            imageBytes.seek(0)
            imageBytes.truncate()
            camera.annotate_text = getOverlayText()
    except KeyboardInterrupt:
        pass
