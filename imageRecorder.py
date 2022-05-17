from io import BytesIO
import time
import datetime
from picamera import PiCamera
import queue

imageQueue = queue.Queue(maxsize=32)

def getOverlayText():
    return "Recording on\n{}".format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

def capture():
    print('Capture thread started')

    # Create the in-memory stream
    camera = PiCamera()
    imageBytes = BytesIO()
    camera.vflip = True
    camera.resolution = (1920, 1080)
    camera.annotate_text_size = 15
    camera.framerate = 10
    camera.annotate_text = getOverlayText()
    camera.start_preview()
    time.sleep(1)

    try:
        i = 1
        start = time.time()

        global imageQueue
        global maxFramerate
        for pic in camera.capture_continuous(imageBytes, 'jpeg', use_video_port=True):
            print('Captured image {} in time {:.2f}s'.format(i, time.time() - start))
            imageQueue.put(imageBytes.getvalue())
            print('Queue size: {}'.format(imageQueue.qsize()))
            print('Saved image {} in time {:.2f}s'.format(i, time.time() - start))

            i += 1
            start = time.time()
            imageBytes.seek(0)
            camera.annotate_text = getOverlayText()
    except KeyboardInterrupt:
        pass
