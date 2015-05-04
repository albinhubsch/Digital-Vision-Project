# -*- coding: utf-8 -*-

"""
	KinectModule

	File contains classes regarding Kinect connection and calculations.

	AUTHOR: albin.hubsch@gmail.com
	UPDATED: 2015-05
"""

# Imports
import requests
import json

class HeadPose(object):
	"""HeadPose 

		represents a headpose, a point in 3D space.
	"""

	def __init__(self, hp_string = None, X = None, Y = None, Z = None):
		"""Constructor of a headpose datatype

			Args:
				hp_string: This is the string containing data for the headpose. String from http api.
			Returns:
				Returns a new headpose struct
			Raises:
				ValueError: Raises a bad value error if the argument has a bad format
		"""
		super(HeadPose, self).__init__()

		if hp_string is None:
			self.X = X
			self.Y = Y
			self.Z = Z
		else:
			try:
				data = hp_string.split(',')
				badArgument = 'Could not create head pose\nBad argument given: must be of format X:0,Y:0,Z:0\n'

				if data[0].split(':')[0] is not 'X' or data[1].split(':')[0] is not 'Y' or data[2].split(':')[0] is not 'Z':
					print badArgument
					raise SystemExit
				else:
					self.X = int(data[0].split(':')[1])
					self.Y = int(data[1].split(':')[1])
					self.Z = int(data[2].split(':')[1])

			except Exception, e:
				raise ValueError

		self.Pitch = self.X
		self.Yaw = self.Y
		self.Roll = self.Z

	def __str__(self):
		""" Return a str version of this point """
		return 'X:'+str(self.X)+',Y:'+str(self.Y)+',Z:'+str(self.Z)

	def getStruct(self):
		""" Return this point as a python struct """
		return {'X': self.Pitch, 'Y': self.Yaw, 'Z': self.Roll}

class KinectConnection(object):
	"""KinectConnection class 
		Fetch headpose from the kinect server
	"""

	def __init__(self, url):
		"""Constructor of a KinectConnection

			Args:
				url: The url to get the data from
			Returns:
				Returns a new server connection
			Raises:
				-
		"""
		super(KinectConnection, self).__init__()
		self.url = url

		try:
			r = requests.get(self.url)
		except Exception, e:
			print 'Could not create connection to the given adress'
			return False

	def fetch(self):
		"""fetch returns latest raw data string from the running Kinect server
		"""
		try:
			r = requests.get(self.url)
			return str(r.text)
		except Exception, e:
			print e
			return False

	def getPose(self):
		"""getPose returns a HeadPose struct with the latest pose from kincet server
		"""
		return HeadPose(self.fetch())