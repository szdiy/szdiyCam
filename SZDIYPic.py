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
from PIL import Image, ImageDraw, ImageFont
from PictureCamera import PictureCamera
import time, os, sys

class SZDIYPic:
	def __init__(self):
		self.aCamera = PictureCamera() #setup a camera instance

	def takeAShot(self,name,width,height):
		self.aCamera.takeAShot(name,width,height);
		#move the pic to tmp directory
		os.system('mv '+name+' '+TMPDIRECTORY)

	def __getPicTimeStampString(self,fileName, fileDirectory, stringFormat):
		fileInfo = os.stat(fileDirectory+'/'+fileName)
		return time.strftime(stringFormat, time.localtime(fileInfo.st_mtime))

	def storeImg(self,fileName, fileDirectory):
		date,time = self.__getPicTimeStampString(fileName, TMPDIRECTORY, '%Y-%m-%d %H.%M.%S').split(' ')

		os.system('mkdir -p ' + imagePath+'/'+date)

		os.system('cp '+fileDirectory+'/'+fileName+' '+imagePath+'/'+date+ '/' + time + '.jpg')

	def resizeImageAndApplyWaterMark (self,inputFileName, outputFileName, quality=85, enWaterMark=True, **waterMarkArgs):
		print "working on img"
		im = Image.open(TMPDIRECTORY+'/'+inputFileName)
		
		if enWaterMark:
			timeInfo = self.__getPicTimeStampString(inputFileName, TMPDIRECTORY, '%Y-%m-%d %H:%M:%S')

			#pass in or define default font parameters
			fontSize = waterMarkArgs['fontSize'] if waterMarkArgs['fontSize'] else 20
			hLocation = waterMarkArgs['hLocation'] if waterMarkArgs['hLocation'] else 10
			vLocation = waterMarkArgs['vLocation'] if waterMarkArgs['vLocation'] else 10

			# use a truetype font
			fontPath = os.path.dirname(os.path.abspath(__file__))+'/'+'KellySlab-Regular.ttf'
			font = ImageFont.truetype(fontPath, fontSize)
			
			print "processing img..."
			draw = ImageDraw.Draw(im)
			draw.text((hLocation, vLocation), timeInfo, font=font)
			del draw

		im.save(TMPDIRECTORY+'/'+outputFileName, 'JPEG', quality=quality)

		del im