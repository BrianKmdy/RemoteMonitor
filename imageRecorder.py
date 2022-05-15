from io import BytesIO
import time
import datetime
from picamera import PiCamera

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

# Create the in-memory stream
camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
stream = BytesIO()
time.sleep(2)

try:
    i = 1
    start = time.time()
    for foo in camera.capture_continuous(stream, 'jpeg', burst=True):
        print('Captured image {} in time {:.2f}s'.format(i, time.time() - start))
        image = ImageOps.flip(Image.open(stream))
        draw = ImageDraw.Draw(image)
        myFont = ImageFont.truetype('cnr.otf', 32)
        draw.text((28, 600), "Recording on\n{}".format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")), font=myFont, fill=(255, 255, 255))

        image.save('capture.jpg')
        print('Saved image {} in time {:.2f}s'.format(i, time.time() - start))
        i += 1
        start = time.time()
        stream.seek(0)
except KeyboardInterrupt:
    pass