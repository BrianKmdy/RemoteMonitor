from io import BytesIO
import time
import datetime
from picamera import PiCamera

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

# Create the in-memory stream
stream = BytesIO()
camera = PiCamera()
camera.start_preview()
time.sleep(0.5)
camera.capture(stream, format='jpeg')
# "Rewind" the stream to the beginning so we can read its content

stream.seek(0)
image = ImageOps.flip(Image.open(stream))
draw = ImageDraw.Draw(image)
myFont = ImageFont.truetype('cnr.otf', 32)
draw.text((28, 600), "Recording on\n{}".format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")), font=myFont, fill=(255, 255, 255))

image.save('image-{}.jpg'.format(int(time.time())))