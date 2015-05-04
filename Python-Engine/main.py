# -*- coding: utf-8 -*-

"""
	PROGRAM:
		Python engine automated kinect camera selections

		This program is a prototype and has the purpose of simulate automated camera selections
		using a kinect and face tracking. This prototype is meant for tv-studios with multiple
		stationary cameras.

	AUTHOR: albin.hubsch@gmail.com
	UPDATED: 2015-05
"""
from KinectModule import HeadPose
from KinectModule import KinectConnection
from BroadcastEnvironment import *
from SetupEnvironment import *
import serial
import time

def main():
	"""Main function

		Starts the program loop and controlls all cameras
	"""

	# Run setup
	s = Setup()
	controlRoom, studio, newscaster = s.beginSetup()

	# Start cameras
	controlRoom.startCameras()
	print 'Cameras started'
	controlRoom.setCameraSize()

	if len(controlRoom.studio.cameras) > 1:
		print 'Everything up and running...'

		# Fetch a camera that best matches the headpose angle
		camera = controlRoom.getClosestCamera()
		while True:
			# If advance camera selection algo indicates true, fetch camera closest to headpose
			if controlRoom.cameraSelectionADV():
				camera = controlRoom.getClosestCamera()
			print 'Active camera: ' + str(camera.cameraID)
			
			# Capture frame or in simulation mode, light up led
			camera.capture()

	elif len(controlRoom.studio.cameras) == 1:
		while True:
			controlRoom.studio.cameras[0].capture()
			time.sleep(2)
	else:
		print 'No cameras found! Something seems to be wrong...'

	# Shutdown all cameras and kill all windows
	controlRoom.shutdownCameras()

if __name__ == "__main__":
	main()