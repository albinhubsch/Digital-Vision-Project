# -*- coding: utf-8 -*-

"""
DOCSTRING
"""

# import cv2
import json
import math
import serial
from KinectModule import HeadPose
from KinectModule import KinectConnection
from statistics import *

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
		""" """
		self.studio = studio

	def startCameras(self):
		"""Start all cameras in the studio"""
		for camera in self.studio.cameras:
			camera.start()
			print 'camera ' + str(camera.cameraID) + ' started'

	def shutdownCameras(self):
		"""Shutdown all cameras in the studio"""
		for camera in self.studio.cameras:
			camera.shutdown()

	def setCameraSize(self, width = 720, height = 481):
		""" """
		for camera in self.studio.cameras:
			camera.setSize(width, height)

	def cameraSelectionADV(self):
		""" Camera selection advanced edition

			Returns: 
				Returns a camera object that should be used for capturing8
		"""

		# Calculate standard deviation from the 20 latest headposes
		num = 5
		
		history = self.studio.newscaster.history[:num]

		# need to calculate the distance between all points in 3D space
		dist_list = []
		for point in history:
			dist_list.insert(0, self.calculateDistanceToHeadpose(point))

		try:
			if stdev(dist_list) < 12:
				return True
			else:
				return False
		except Exception, e:
			return False

	def getClosestCamera(self):
		""" Get the choosen camera from the sudio 
			The choosen camera is the one that the newscaster is currently facing

			Returns:
				Returns a camera object
		"""
		# Fetch current headpose of newscaster
		headpose = self.studio.newscaster.getHeadpose()

		# We need all cameras and their position
		cameras = self.studio.cameras

		# Find shortest euklidian distance to any camera position from the headpose
		short_v = self.calculateDistanceToHeadpose(cameras[0].position)
		close_cam = cameras[0]
		for camera in cameras:
			v = self.calculateDistanceToHeadpose(camera.position)
			if v <= short_v:
				short_v = v
				close_cam = camera

		# Return the closest camera
		return close_cam

	def calculateDistanceToHeadpose(self, position):
		headpose = self.studio.newscaster.getHeadpose()
		return math.sqrt( (abs(position.X - headpose.X))**2 + (abs(position.Y - headpose.Y))**2 + (abs(position.Z - headpose.Z))**2 )

	def calculateDistanceBetween2Headpose(headpose1, headpose2):
		return math.sqrt( (abs(headpose1.X - headpose2.X))**2 + (abs(headpose1.Y - headpose2.Y))**2 + (abs(headpose1.Z - headpose2.Z))**2 )

class Camera(object):
	"""docstring for Camera
	"""
	def __init__(self, cameraID, position = None):
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

	def toString(self):
		""" Returns stringification of the camera object """
		return str({"id": self.cameraID, "position": str(self.position)})

	def getJsonObj(self):
		return {"id": self.cameraID, "position": self.position.getStruct()}

	def start(self):
		"""Start this camera for capturing frames

			Returns:
				True or False
		"""
		print 'Starting cam ' + str(self.cameraID)
		try:
			# self.capObj = cv2.VideoCapture(self.cameraID)
			return True
		except Exception, e:
			return False

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

class Camera_E(object):
	"""This is the emulated camera for arduino
	"""
	def __init__(self, cameraID, position = None, serial_link = None):
		"""Constructor creating a new camera object

			Args:
				cameraID: The ID for the camera connected to the computer
				position: The position of the camera given in a HeadPose
			Returns:
				Returns a new camera object
			Raises:
				-
		"""
		super(Camera_E, self).__init__()

		self.cameraID = cameraID
		self.position = position
		self.capObj = None
		self.serial_link = serial_link

	def toString(self):
		""" Returns stringification of the camera object """
		return str({"id": self.cameraID, "position": str(self.position)})

	def getJsonObj(self):
		return {"id": self.cameraID, "position": self.position.getStruct()}

	def start(self):
		"""Start this camera for capturing frames

			Returns:
				True or False
		"""
		pass

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
		pass

	def capture(self):
		"""Captures a frame from this camera

			Returns:
				Returns a frash frame from the camera
		"""
		# print 'writing to arduino: '+str(self.cameraID)+','
		self.serial_link.write(str(self.cameraID)+',')

	def shutdown(self):
		"""Release this camera from video capture
		"""
		pass
		

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
		self.history = []
		
	def getHeadpose(self):
		"""
		"""
		return self.setHeadpose(self.kinectConn.getPose())

	def setHeadpose(self, headpose):
		"""
		"""
		self.addToHistory(headpose)
		self.headpose = headpose
		return self.headpose

	def addToHistory(self, headpose):
		""" 
		"""
		if len(self.history) < 120:
			self.history.insert(0, headpose)
		else:
			self.history.pop()
			self.addToHistory(headpose)