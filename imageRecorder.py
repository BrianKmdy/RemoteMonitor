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
camera.resolution = (640, 480)
camera.start_preview()
time.sleep(2)

while True:
    stream = BytesIO()
    camera.capture(stream, format='jpeg')
    image = ImageOps.flip(Image.open(stream))
    draw = ImageDraw.Draw(image)
    myFont = ImageFont.truetype('cnr.otf', 32)
    draw.text((28, 600), "Recording on\n{}".format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")), font=myFont, fill=(255, 255, 255))

    image.save('capture.jpg'.format(int(time.time())))
    time.sleep(0.1)