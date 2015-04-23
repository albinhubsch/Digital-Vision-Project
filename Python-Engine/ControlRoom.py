# -*- coding: utf-8 -*-

"""
DOCSTRING
"""

import cv2
from KinectModule import HeadPose

class Camera(object):
	"""docstring for Camera
	"""
	def __init__(self, cameraID, position):
		"""Constructor creating a new camera object

			Args:
				cameraID: The ID for the camera connected to the computer
				position: The position of the camera given in a HeadPose
			Returns:
				Returns a new camera object
			Raises:
				-
		"""
		super(Camera, self).__init__()

		self.cameraID = cameraID
		self.position = position
		self.capObj = None

	def start(self):
		"""Start this camera for capturing frames

			Returns:
				True or False
		"""
		try:
			self.capObj = cv2.VideoCapture(self.cameraID)
			return True
		except Exception, e:
			return False

	def getPosition(self):
		"""Returns this cameras position"""
		return self.position

	def setPosition(self, position):
		"""Set the position of this camera"""
		self.position = position

	def updatePosition(self, position):
		"""Update the position for this camera"""
		self.setPosition(position)

	def setSize(self, width, height):
		"""Set the video capture size

			Args:
				width: The pixel width
				height: The pixle height
		"""
		self.capObj.set(3, width)
		self.capObj.set(4, height)

	def capture(self):
		"""Captures a frame from this camera

			Returns:
				Returns a frash frame from the camera
		"""
		try:
			ret, frame = self.capObj.read()
			if ret:
				return frame
			else:
				return False
		except Exception, e:
			return False

	def shutdown(self):
		"""Release this camera from video capture
		"""
		self.capObj.release()