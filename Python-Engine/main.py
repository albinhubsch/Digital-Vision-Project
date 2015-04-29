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


	# Start cameras
	controlRoom.startCameras()
	print 'Cameras started'
	controlRoom.setCameraSize()

	if len(controlRoom.studio.cameras) > 1:
		print 'Everything up and running...'
		while True:
			camera = controlRoom.getClosestCamera()
			print camera.cameraID
			# camera.capture()
			time.sleep(0.05)

	elif len(controlRoom.studio.cameras) == 1:
		while True:
			controlRoom.studio.cameras[0].capture()
			time.sleep(2)
	else:
		print 'No cameras found! Something seems to be wrong...'

	# Shutdown all cameras and kill all windows
	controlRoom.shutdownCameras()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()