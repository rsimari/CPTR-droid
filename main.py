import serial
import time
from light_controller import LightController
import face_controller 
import subprocess as sp
import picamera
import pickle
import os
import signal

print('libs loaded')
port = serial.Serial('/dev/ttyAMA0', baudrate=9600)

camera = picamera.PiCamera()
fc = face_controller.FaceController(camera)

os.system("xte 'mousemove 0 600'")
if port.is_open:
	print("/dev/ttyAMA0 is open")

lc = LightController()
stop = 0 # possibly have a flag that will terminate any routine

def take_picture():
	pid = os.fork()
	if pid == 0:
		# in child process
		lc.pic_countdown()
		os._exit(0)
	else:
		# in parent
		camera.start_preview()
		time.sleep(4)
		name = str(time.time()) + '_pic.jpg'
		camera.capture(name)	
		camera.stop_preview()
		#os.system("echo 'tkean by T4-K3' | mail -s 'Droid Pic' -a " + str(name) + "royce5branning@yahoo.com")
		os.wait()
	print('picture taken')

def scan():
	pid = os.fork()
	if pid == 0:
		# in child process
		while True:
			lc.scan()
		os._exit(0)
	else:
		names = fc.scan_for_faces()	
		if names != None:
			print(names)
		# stop child
		os.kill(pid, signal.SIGKILL)
		os.wait()
		if names != None:
			print("SUCCESS")
			lc.scan_success() 

	lc.clear()
	print('done scanning')

print('ready...')

try:
	while True:
		while port.in_waiting == 0: time.sleep(0.1)
		c = port.read()
		print('received ' + str(c))
		if c == b'x':
			take_picture()
		elif c == b'y':
			scan()
except KeyboardInterrupt:
	port.close()

