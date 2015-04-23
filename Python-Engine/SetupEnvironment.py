# -*- coding: utf-8 -*-

"""
DOCSTRING
"""

import cv2
import os
from BroadcastEnvironment import *
from Tkinter import *
import time

class Setup(object):
	"""docstring for Setup
	"""

	def __init__(self):
		super(Setup, self).__init__()

		# 
		self.beginSetup()

	def beginSetup(self):
		"""beginSetup
		"""
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

			# 
			# Start camera recording here
			# 

			print 'Look into the camera currently recording.\nWhen ready to calibrate press Enter. Keep your head steady for 3 seconds.'
			raw_input('')

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

			print 'Camera calibrated'



def cl():
		os.system(['clear','cls'][os.name == 'nt'])