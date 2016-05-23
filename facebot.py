import io
import picamera
import cv2
import numpy
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import datetime

from facenav import closest_face, facedrive

#config
show_video = False

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 3
rawCapture = PiRGBArray(camera, size=(320, 240))

#Load a cascade file for detecting faces
#face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml') #accurate but slow
face_cascade = cv2.CascadeClassifier('/usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml') #faster but less accurate

# allow the camera to warmup, then initialize the average frame, last
# uploaded timestamp, and frame motion counter
print "[INFO] warming up..."
time.sleep(0.5)
avg = None

# initialize the timestamp
last_timestamp = datetime.datetime.now()

# Sample face - x,y,w,h from lower left
test_faces=[[ 83,  27, 167, 167]]

# capture frames from the camera
for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image and initialize
    # the timestamp and occupied/unoccupied text
    frame = f.array
    timestamp = datetime.datetime.now()
    timedelta = timestamp - last_timestamp
    last_timestamp = timestamp

    print str(timedelta.total_seconds())

    # convert it to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Look for faces in the image using the loaded cascade file - this is extreamly slow.
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    print "Found "+str(len(faces))+" face(s)"

    # Select closest face
    face = closest_face(faces)
    
    # This is a cumbersome test to see if there is a face
    if not isinstance(face, bool):
        # If a face exists, commence menacing driving    
        facedrive(face)



    # check to see if the frames should be displayed to screen
    if show_video:
        # display the security feed
        cv2.imshow("Faces", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
