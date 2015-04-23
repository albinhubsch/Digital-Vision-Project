# -*- coding: utf-8 -*-

"""
DOCSTRING
"""
from KinectModule import HeadPose
from KinectModule import KinectConnection
from BroadcastEnvironment import *
from SetupEnvironment import *

import cv2
import numpy as np

def main():
	"""Description of function goes here

		Args:
			n: Argument description
		Returns:
			Description of the return value
		Raises:
			Exception: Description of the exception that can be raised
	"""

	e = Setup()

	# n = HeadPose("X:20,Y:10,Z:32");

	# # s = KinectConnection('http://localhost:8080')
	# # print s.getPose().Roll
	
	# cam1 = Camera(0, n)
	# cam1.start()
	# cam1.setSize(320, 240)


	# while(True):
	#     # Capture frame-by-frame
	#     frame = cam1.capture()

	#     # Our operations on the frame come here
	#     # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	#     # Display the resulting frame
	#     cv2.imshow('frame',frame)
	#     if cv2.waitKey(1) & 0xFF == ord('q'):
	#         break

	# # When everything done, release the capture
	# cam1.shutdown()
	# cv2.destroyAllWindows()

if __name__ == "__main__":
	main()