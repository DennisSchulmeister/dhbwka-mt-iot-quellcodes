#! /usr/bin/env python3

"""
Minimalbeispiel zur Nutzung der Pi-Kamera.
Vgl. https://github.com/raspberrypi/picamera2/blob/main/examples/capture_headless.py

Viele weitere Beispiele unter:
https://github.com/raspberrypi/picamera2/tree/main/examples

Vgl. https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
"""

from picamera2 import Picamera2
from libcamera import Transform

picam2 = Picamera2()
config = picam2.create_still_configuration(transform=Transform(vflip=True))
picam2.configure(config)

picam2.start()

#np_array = picam2.capture_array()
#print(np_array)
picam2.capture_file("demo.jpg")
picam2.stop()