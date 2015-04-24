# -*- coding: utf-8 -*-

"""
DOCSTRING
"""

import cv2
import os
import json
from BroadcastEnvironment import *
from Tkinter import *
import time

class Setup(object):
	"""docstring for Setup
	"""

	def __init__(self):
		super(Setup, self).__init__()

	def beginSetup(self):
		"""beginSetup
		"""
		cl()
		print 'Menu\n1. Load Broadcast Environment from a json file\n2. Create a new configuration and camera calibration\n'
		choice = int(raw_input('Type your choice from the menu above: '))

		if choice is 1:
			jsonFile = str(raw_input('Type the name of the json file: '))
			with open(jsonFile+'.json') as data_file:
				data = json.load(data_file)

			newscaster = Newscaster(data['Newscaster']['name'], data['Newscaster']['url'])
			cameras = []
			for camera in data['cameras']:
				cameras.append(Camera(camera['id'], HeadPose(X=camera['position']['X'], Y=camera['position']['Y'], Z=camera['position']['Z'])))
			studio = Studio(cameras, newscaster)
			controlRoom = ControlRoom(studio)

			print '\nSetup was loaded successfully\n'

		else:
			cl()
			number_of_cameras = int(raw_input('Please type in the number of cameras in your studio: '))
			cl()
			newscaster_name = str(raw_input('Please type in the name of the newscaster: '))
			cl()
			newscaster_url = str(raw_input('Please type in the adress to '+newscaster_name+': '))
			cl()
			print '!! Creating newscaster...'
			try:
				newscaster = Newscaster(newscaster_name, newscaster_url)
			except Exception, e:
				print 'Could not create newscaster'
				print e
				raise SystemExit
			print '== Newscaster created =='

			print '!! Building cameras...'
			cameras = []
			for i in xrange(number_of_cameras):
				cameras.append(Camera(i, None))
			print '== Cameras built =='
			print '!! Renovating studio...'
			studio = Studio(cameras, newscaster)
			print '== Studio ready =='
			print '!! Booting Control room...'
			controlRoom = ControlRoom(studio)
			print '== Control room is ready =='

			print '\n'

			# Okey, now it's time for calibrating the cameras...

			print '!!! THERE ARE '+str(number_of_cameras)+' CAMERAS THAT NEEDS TO BE CALIBRATED !!!'
			raw_input('Press Enter when ready to begin calibration...')
			for camera in controlRoom.studio.cameras:

				print 'Starting camera'

				camera.start()
				camera.setSize(320, 240)

				print 'Look into this camera and press q when ready. Hold your head steady for 3 seconds while calibrating'

				while(True):
					frame = camera.capture()
					# Display the resulting frame
					cv2.imshow('frame',frame)
					if cv2.waitKey(1) & 0xFF == ord('q'):
						break

				camera.shutdown()
				cv2.destroyAllWindows()

				print 'Calibrating...'

				calib_list = []
				for x in xrange(60):
					calib_list.append(newscaster.getHeadpose())
					time.sleep(0.05)

				sumx = 0
				sumy = 0
				sumz = 0

				for hp in calib_list:
					sumx += hp.X
					sumy += hp.Y
					sumz += hp.Z

				# Set camera position
				camera.setPosition(HeadPose(X = sumx/60, Y = sumy/60, Z = sumz/60))

				print 'Camera calibrated\n'

			print 'Writing config to file: env.json'
			# Write config to json file
			prep_cameras_for_json = []
			for cam in cameras:
				prep_cameras_for_json.append(cam.getJsonObj())
			js = {'Newscaster': {'name': newscaster_name, 'url': newscaster_url}, 'cameras': prep_cameras_for_json}
			with open('env.json', 'w') as outfile:
				json.dump(js, outfile)

			print '\n== Calibration and Configuration completed ==\n'

		return controlRoom, studio, newscaster

def cl():
		os.system(['clear','cls'][os.name == 'nt'])