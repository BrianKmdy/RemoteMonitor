from io import BytesIO
import time
import datetime
from picamera import PiCamera
import collections

frameRate = 16
frameCount = 0

maxQueueSize = int(frameRate * 1)
imageQueue = collections.deque(maxlen=maxQueueSize)

def getOverlayText():
    return "Recording on\n{}".format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

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
    camera.resolution = (640, 480)
    camera.annotate_text_size = 18
    camera.framerate = frameRate
    camera.annotate_text = getOverlayText()
    camera.start_preview()
    time.sleep(1)

    try:
        start = time.time()
        for frame in camera.capture_continuous(imageBytes, 'jpeg', use_video_port=True):
            print('Captured image {} in time {:.2f}s'.format(frameCount, time.time() - start))
            imageQueue.append(imageBytes.getvalue())
            print('Queue size: {}'.format(len(imageQueue)))
            print('Saved image {} in time {:.2f}s'.format(frameCount, time.time() - start))

            frameCount += 1
            start = time.time()
            imageBytes.seek(0)
            camera.annotate_text = getOverlayText()
            if len(imageQueue) >= maxQueueSize:
                time.sleep(0.05)
    except KeyboardInterrupt:
        pass
