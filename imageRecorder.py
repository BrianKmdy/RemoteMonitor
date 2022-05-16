from io import BytesIO
import time
import datetime
from picamera import PiCamera
import queue

imageQueue = queue.Queue()

def getOverlayText():
    return "Recording on\n{}".format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

def capture():
    print('Capture thread started')

    # Create the in-memory stream
    camera = PiCamera()
    imageBytes = BytesIO()
    camera.resolution = (640, 480)
    camera.annotate_text_size = 15
    camera.start_preview()
    camera.annotate_text = getOverlayText()
    time.sleep(2)

    try:
        i = 1
        start = time.time()

        global imageQueue
        for foo in camera.capture_continuous(imageBytes, 'jpeg', use_video_port=True):
            print('Captured image {} in time {:.2f}s'.format(i, time.time() - start))
            imageQueue.put(imageBytes.getvalue())
            print('Saved image {} in time {:.2f}s'.format(i, time.time() - start))

            i += 1
            start = time.time()
            imageBytes.seek(0)
            camera.annotate_text = getOverlayText()
    except KeyboardInterrupt:
        pass