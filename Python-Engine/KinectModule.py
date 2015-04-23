# -*- coding: utf-8 -*-

"""
DOCSTRING
"""

# Imports
import requests

class HeadPose(object):
	"""Description of object goes here
	"""

	def __init__(self, hp_string):
		"""Constructor of a headpose datatype

			Args:
				hp_string: This is the string containing data for the headpose. String from http api.
			Returns:
				Returns a new headpose struct
			Raises:
				ValueError: Raises a bad value error if the argument has a bad format
		"""
		super(HeadPose, self).__init__()

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
				self.Pitch = self.X
				self.Yaw = self.Y
				self.Roll = self.Z

		except Exception, e:
			raise ValueError


class KinectConnection(object):
	"""Description
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