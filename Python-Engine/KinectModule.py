# -*- coding: utf-8 -*-

"""
DOCSTRING
"""

class HeadPose(object):
	"""Description of object goes here

		Args:
			n: Argument description
		Returns:
			Description of the return value
		Raises:
			Exception: Description of the exception that can be raised
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

			print self.X
		except Exception, e:
			raise ValueError
