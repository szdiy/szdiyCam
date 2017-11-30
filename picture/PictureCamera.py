# Copyright (C) 2014 SZDIY Hackers' Community
#
# This file is part of szdiyCam.
#
# szdiyCam is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# szdiyCam is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with szdiyCam.  If not, see <http://www.gnu.org/licenses/>.

import os, traceback
import time


# A list of camera drivers:
#  - pygame.camera
#  		depend on SDL, only supports Linux and v4l2 cameras.
#  		You may find windows support on third party build.
#
#  - PiCamera
#  		only supported on Raspberry Pi platform.
#
#  - OpenCV
#		supports OSX ( `$ brew install opencv`), the installation is tricky, not lightweight.
#
#  - GStreamer and gst-python
#  		The brew package on OSX is too old and doesn't have video capture components
#


# try to import different camera drivers
try:
	import picamera
except:
	picamera = False

try:
	import cv2
except:
	cv2 = False

class CameraDriver:

	def takeAShot(self,name,width,height):
		raise RuntimeError('Use concrete class instead!')

	# list of methods testifying camera drivers
	@classmethod
	def test_picamera(clz):
		return picamera

	@classmethod
	def test_cv2(clz):
		return cv2


class PiCamera(CameraDriver):
	def __init__(self):
		pass

	def takeAShot(self,name,width,height):
		self.camera = picamera.PiCamera()
		self.camera.resolution = (width,height)

		self.camera.ISO = 0
		self.camera.meter_mode = 'matrix'
		self.camera.exposure_mode = 'auto'
		self.camera.awb_mode='auto'

		try:
			time.sleep(2) #camera warm up time, otherwise you get dark picture
			self.camera.capture(name, format='jpeg')
		except:
			print "capture error"
		self.camera.close()


class CV2Camera(CameraDriver):
	def __init__(self):
		pass

	def takeAShot(self, name, width, height):
		self.camera = cv2.VideoCapture(0) # 0 is the integrated camera on the computer

		try:
			time.sleep(2) # camera warm up, otherwise you get dark picture
			ret, img = self.camera.read()
			if ret:
				# TODO: convert image size and other properties
				cv2.imwrite(name, img)
		except:
			traceback.print_stack()

		self.camera.release()



class PictureCamera:
	"""A wrapper class for camera"""

	def __init__(self):
		# detect which camera driver is available
		if CameraDriver.test_picamera():
			self.camera = PiCamera()
		elif CameraDriver.test_cv2():
			self.camera = CV2Camera()
		else:
			raise RuntimeError('No suitable camera driver found.')

	def takeAShot(self, name, width, height):
		self.camera.takeAShot(name, width, height)
