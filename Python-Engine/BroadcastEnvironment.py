# -*- coding: utf-8 -*-

"""
DOCSTRING
"""

import cv2
from KinectModule import HeadPose
from KinectModule import KinectConnection

class Studio(object):
	"""docstring for Studio
	"""
	def __init__(self, cameras = [], newscaster = None):
		super(Studio, self).__init__()

		self.cameras = cameras #Allocate memory for cameras in studio
		self.newscaster = newscaster

	def installCamera(self, camera):
		"""Install a new camera in the studio
			
			Args:
				camera: The camera that should be installed
		"""
		self.cameras.append(camera)

	def cameras(self):
		"""Returns a list with all cameras in the studio
		"""
		return self.cameras

	def newscaster(self):
		"""
		"""
		return self.newscaster

	def setNewscaster(self, newscaster):
		"""
		"""
		self.newscaster = newscaster


class ControlRoom(object):
	"""docstring for ControlRoom
	"""
	
	def __init__(self, studio = None):
		"""Create a new ControlRoom. The control room controls all cameras in the studio
		and also do the choice of which camera to choose

			Args: 
				asd
		"""
		super(ControlRoom, self).__init__()
		self.studio = studio

	def linkStudio(self, studio):
		self.studio = studio

	def startCameras(self):
		"""Start all cameras in the studio"""
		for camera in self.studio.cameras:
			camera.start()

	def shutdownCameras(self):
		"""Shutdown all cameras in the studio"""
		for camera in self.studio.cameras:
			camera.shutdown()


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

class Newscaster(object):
	"""docstring for Newscaster
	"""

	def __init__(self, name, url):
		"""
		"""
		super(Newscaster, self).__init__()
		self.name = name
		self.headpose = None
		self.kinectConn = KinectConnection(url)
		
	def headpose(self):
		"""
		"""
		return self.setHeadpose(self.kinectConn.getPose())

	def setHeadpose(self, headpose):
		"""
		"""
		self.headpose = headpose
		return self.headpose