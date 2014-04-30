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

from config import TMPDIRECTORY, imagePath
from PIL import Image, ImageDraw
from PictureCamera import PictureCamera
import time, os, sys

class SZDIYPic:
	def __init__(self):
		self.aCamera = PictureCamera() #setup a camera instance

	def takeAShot(self,name,width,height):
		self.aCamera.takeAShot(name,width,height);
		#move the pic to tmp directory
		os.system('mv image.jpg '+TMPDIRECTORY)

	def __storeImg(self,finalFileName, timeStampString):
		timeInfo = timeStampString.split(' ')
		date=timeInfo[0];
		time=timeInfo[1];

		os.system('mkdir -p ' + imagePath+'/'+date)

		timeArray = time.split(':')
		fileName = timeArray[0]+'.'+timeArray[1]+'.'+timeArray[2]+'.jpg'
		os.system('cp '+TMPDIRECTORY+'/'+finalFileName+' '+imagePath+'/'+date+ '/' + fileName)

	def resizeImageAndApplyWaterMark (self,inputFileName, outputFileName, quality, enableStoreImage):
		print "working on img"
		im = Image.open(TMPDIRECTORY+'/'+inputFileName)
		draw = ImageDraw.Draw(im)
		textPadding = 5
		topLeftWidth = int(im.size[0] - (im.size[0] / 4))
		topLeftHeight = int(im.size[1] - (im.size[1] / 10))
		fileInfo = os.stat(TMPDIRECTORY+'/'+inputFileName)
		timeInfo = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(fileInfo.st_mtime))

		print "processing img..."
		draw.text([topLeftWidth + textPadding, topLeftHeight + textPadding], timeInfo, fill="green")
		im.save(TMPDIRECTORY+'/'+outputFileName, 'JPEG', quality=quality)

		#storage image to a archive folder
		if enableStoreImage:
			self.__storeImg(outputFileName,timeInfo)
		
		del draw
		del im