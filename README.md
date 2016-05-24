# Facebot

A little raspberry pi based robot that lurches menacingly toward human faces.
The OpenCV code code is cobbled together from various openCV demos on http://www.pyimagesearch.com/

![Facebot](/images/facebot.jpg?raw=true "The Menacing Facebot")

## Bits and pieces

* Rasperry pi 2 or 3
  * Running rasbian Jessie
    * Wheezy won't work unless you feel like compiling openCV - which takes hours.
* [raspirobotboard](https://github.com/simonmonk/raspirobotboard/wiki)
  * These are actually not very good -  but it is what this code works with.
  A much better idea would be the
  [version 3](https://github.com/simonmonk/raspirobotboard3) of this
  board - it adds a switch
  mode power supply so it won't get so hot, and allows you to speed control the motors!
    * The code would be similar.
* A robot chassis and motors
  * I used a Magician Chassis - I used [this one](http://www.mindkits.co.nz/store/p/9281-2WD-Mobile-platform-Kit.aspx?status=1)
  from mindkits.  You could self source the bits for less from ebay - or 3D print something.  On the other hand, the mindkits people are very nice.
    * Also note that the motors that come with this kit are designed for about 5V - we will run them at a bit more than that, reducing their life.
    * The also don't have power leads attached so you'll need to solder or crimp some wire on.
* [A rasperry pi camera](http://www.mindkits.co.nz/camera-module-with-color-cmos-qsxga-for-raspberry-pi.aspx?status=1).  
  * In hindsight the rasperry pi camera doesn't really add anything - it is nice as it has more
  bandwidth than a usb 2 interface and has low latency - however the facial detection code is so slow that these advantages are lost.  If you have webcam lying around, try that first I think it could be made to work just as well.
  * I 3D printed [this mount, case and hinge](http://www.thingiverse.com/thing:239268) for it
* some kind of usb wireless dongle, unless you are using the pi3 in which case that is built in.

## The code

### Install dependancies

Note that best practise is to install the python dependancies with pip and use [python virtualenvs](http://docs.python-guide.org/en/latest/dev/virtualenvs/).  However for the sake of simplicity, this just installs all the dependancies system wide.
#### System dependancies
```bash
sudo apt-get install libopencv-dev python-opencv
sudo apt-get install python-numpy
sudo pip install rpio
sudo pip install picamera  # not if using a webcam
sudo pip install 'picamera[array]' #not if using a webcam
```

#### Raspirobot library
```bash
wget https://github.com/simonmonk/raspirobotboard/archive/master.zip # different if using a version2 or 3
unzip master.zip
cd raspirobotboard-master
sudo python setup.py install
```

#### Facebot project

Either get the project zip
```bash
cd ~
wget https://github.com/andre-geldenhuis/facebot/archive/master.zip
unzip master.zip  # project is in facebot-master
```
Or clone the github repository
```bash
git clone https://github.com/andre-geldenhuis/facebot.git
```

## Test the robot mechanics

SSH into the robot. Alternativly you could use a keyboard, mouse and a monitor - though this won't work once you have it driving around!

Start an interactive python interpreter:
```bash
python
```
In the interpreter:
```python
from raspirobotboard import *
rr = RaspiRobot()

# Test the motors both turn in the correct direction to drive the robot forward
# 0.3 drives for 0.3 seconds -  this helps stop the robot driving off your desk!
# If the motors turn in the wrong direction, swap the wire around for the offending motor
rr.forward(0.3)

# Test the motors are wired correctly left and right.
# This test is easier with the bot facing away from you.
# The left motor should driving that wheel backward
# the right motor should drive that wheek forward
# if not, swap the motor connectors over.
rr.left(0.3)
```




## Running the robot.

SSH into the robot and change to the Facebot project directory. Run the project
```bash
python facebot
```

It should now lurch toward human faces - if it doesn't work well (and it won't) it'll need tuning.

## Tuning
This robot doesn't work very well - the simple proportional controller settings need to be tuned.
If you have version 3 of the raspirobotboard you could try use PWM speed control on the motors rather than controlling the motor run times.

The proportional controller settings are in the facenav.py file

There are two possible face detection cascades you can use, the haar cascade is much better,  but much slower - you'll be lucky to get 1 frame per second processed.  The lbp cascade is about 3-4x faster but is much less good at detecting faces.  You can select which one to use by commenting out the corresponding lines in facebot.py

Note that you proportioanl controller gain K will probably need to be a bit different depending on which cascade you are using as the process time will effect the controller responsivess and stability.
