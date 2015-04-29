# -*- coding: utf-8 -*-

"""
DOCSTRING
"""
from KinectModule import HeadPose
from KinectModule import KinectConnection
from BroadcastEnvironment import *
from SetupEnvironment import *

import serial
import cv2
import numpy as np
import time

def main():
	"""Description of function goes here

		Args:
			n: Argument description
		Returns:
			Description of the return value
		Raises:
			Exception: Description of the exception that can be raised
	"""

	# Serial link for camera emulation
	# serial_link = serial.Serial('COM5', 9600)

	# Run setup
	s = Setup()
	controlRoom, studio, newscaster = s.beginSetup()

	# Create a window
	cv2.namedWindow('Live', flags=cv2.WINDOW_OPENGL)
	cv2.resizeWindow('Live', 720, 481)
	cv2.moveWindow('Live', 240, 240)


	# Start cameras
	controlRoom.startCameras()
	print 'Cameras started'
	controlRoom.setCameraSize()

	if len(controlRoom.studio.cameras) > 1:
		# pass

		while True:
			time.sleep(3)
			print 'varvning'

		# while(True):
			# Fetch headpose from newscaster
			# pose = newscaster.getHeadpose()

			# Get camera based on pose
			# camera =  controlRoom.getClosestCamera()
			
			# frame = camera.capture()
			# cv2.imshow('Live', frame)
			# if cv2.waitKey(1) & 0xFF == ord('q'):
			# 	break

	elif len(controlRoom.studio.cameras) == 1:
		while(True):
			frame = controlRoom.studio.cameras[0].capture()
			cv2.imshow('Live', frame)
			
			# Listen for ESC key, leave loop if pressed
			k = cv2.waitKey(1) & 0xFF
			if k == 27:
				break
	else:
		print 'No cameras found! Something seems to be wrong...'

	# Shutdown all cameras and kill all windows
	controlRoom.shutdownCameras()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()