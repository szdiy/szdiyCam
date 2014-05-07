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

import os
import picamera
import time

class PictureCamera:
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
			time.sleep(2) #camera warm up time
			self.camera.capture(name, format='jpeg')
		except:
			print "capture error"
		self.camera.close()