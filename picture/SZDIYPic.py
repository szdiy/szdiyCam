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

from config import TMPDIRECTORY, TMPIMAGE, IMAGE_PATH
from PIL import Image, ImageDraw, ImageFont
from picture.PictureCamera import PictureCamera
import time, os, sys

class SZDIYPic:
	def __init__(self):
		self.aCamera = PictureCamera() #setup a camera instance

	def takeAShot(self,name,width,height):
		outputName = os.path.join(TMPDIRECTORY, name)
		self.aCamera.takeAShot(outputName,width,height);
		return outputName
		#move the pic to tmp directory
		# os.system('mv '+name+' '+TMPDIRECTORY)

	def __getPicTimeStampString(self,fileName, fileDirectory, stringFormat):
		fileInfo = os.stat(fileDirectory+'/'+fileName)
		return time.strftime(stringFormat, time.localtime(fileInfo.st_mtime))

	def storeImg(self,fileName, fileDirectory):
		date,time = self.__getPicTimeStampString(fileName, TMPDIRECTORY, '%Y-%m-%d %H.%M.%S').split(' ')

		os.system('mkdir -p ' + IMAGE_PATH+'/'+date)

		os.system('cp '+fileDirectory+'/'+fileName+' '+IMAGE_PATH+'/'+date+ '/' + time + '.jpg')

	def __copyEXIF(self,originalImagePath,destinationImagePath):
		try:
			import pyexiv2
		except ImportError:
			print "pyexiv2 is not installed correctly, exif data won't be correct"
			return

		sourceImage = pyexiv2.metadata.ImageMetadata(originalImagePath)
		destinationImage = pyexiv2.metadata.ImageMetadata(destinationImagePath)
		sourceImage.read() #required to process the exif data
		destinationImage.read() #required to process the exif data
		sourceImage.copy(destinationImage)

		image = Image.open(destinationImagePath)
		destinationImage["Exif.Photo.PixelXDimension"] = image.size[0]
		destinationImage["Exif.Photo.PixelYDimension"] = image.size[1]
		destinationImage.write()
		del image

	def compressImageAndApplyWaterMark (self,inputFileName, outputFileName, quality=85, enWaterMark=True, **waterMarkArgs):
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
		self.__copyEXIF(TMPDIRECTORY+'/'+inputFileName,TMPDIRECTORY+'/'+outputFileName) #copy the exif data over

		del im


if __name__ == "__main__":
	# Testing if screen capture is working
	snapshot = SZDIYPic()
	outputName = snapshot.takeAShot(TMPIMAGE,800,600)
	print('image saved at: {}'.format(outputName))
