import picamera
import time

camera = picamera.PiCamera()

for i in range(5) :
  camera.capture("../static/images/%d.jpg" % i)
  time.sleep(0.1)

camera.close()