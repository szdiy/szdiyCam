i# Copyright (C) 2014 SZDIY Hackers' Community

# This file is part of szdiyCam.

# szdiyCam is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# szdiyCam is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with szdiyCam.  If not, see <http://www.gnu.org/licenses/>.

# from resizeImageAndApplyWaterMark import resizeImageAndApplyWaterMark
from PIL import Image, ImageDraw
from uploadToQiNiu import uploadToQiNiu
from takeAShot import PictureCamera
import time, os, sys, requests
from credentials import LinodeServerImageUploadAPIURL

TMPDIRECTORY  = '/tmp'
imagePath = '/home/pi/szdiy_img'

def uploadToLinode(files):
	print "uploading image"
	requests.post(LinodeServerImageUploadAPIURL,files=files, timeout=20) #time out at 20 secs
	print "image upload complete"


def storeImg(finalFileName, timeStampString):
	timeInfo = timeStampString.split(' ')
	date=timeInfo[0];
	time=timeInfo[1];

	os.system('mkdir -p ' + imagePath+'/'+date)

	timeArray = time.split(':')
	fileName = timeArray[0]+'.'+timeArray[1]+'.'+timeArray[2]+'.jpg'
	os.system('cp '+TMPDIRECTORY+'/'+finalFileName+' '+imagePath+'/'+date+ '/' + fileName)

def resizeImageAndApplyWaterMark (inputFileName, outputFileName, quality, enableStoreEmage):
	print "working on img"
	im = Image.open(TMPDIRECTORY+'/'+inputFileName)
	draw = ImageDraw.Draw(im)
	textPadding = 5
	topLeftWidth = int(im.size[0] - (im.size[0] / 4))
	topLeftHeight = int(im.size[1] - (im.size[1] / 10))
	fileInfo = os.stat(TMPDIRECTORY+'/'+inputFileName)
	timeInfo = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(fileInfo.st_mtime))
	if enableStoreEmage:
		storeImg(outputFileName,timeInfo)

	print "processing img..."
	draw.text([topLeftWidth + textPadding, topLeftHeight + textPadding], timeInfo, fill="green")
	im.save(TMPDIRECTORY+'/'+outputFileName, 'JPEG', quality=quality)
	del draw
	del im

aCamera = PictureCamera() #setup a camera instance
while True:
	aCamera.takeAShot('image.jpg',800,600);
	#move the pic to tmp
	os.system('mv image.jpg '+TMPDIRECTORY)

	resizeImageAndApplyWaterMark ('image.jpg', 'new.jpg', 80, False)

	aFile = open(TMPDIRECTORY+'/'+'new.jpg', 'rb')
	files = {'file': aFile}
	try:
		uploadToLinode(files)
	except:
		print "Network seems down, try again in 20sec..."

	time.sleep(1)


	
	aCamera.takeAShot('image.jpg',1024,768);
	#move the pic to tmp
	os.system('mv image.jpg '+TMPDIRECTORY)

	resizeImageAndApplyWaterMark('image.jpg','new.jpg',95, True)
	print "upload to qiniu"
	try:
		uploadToQiNiu('szdiy','new.jpg',TMPDIRECTORY)
	except:
		print "uploadToQiNiu failed"

	time.sleep(20)

	
