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
from SZDIYPic import SZDIYPic
from WX import WX
from uploadToLinode import uploadAFileToLinodeWithWXMediaID
from uploadToQiNiu import uploadingAFileToQiNiu
import time

def setDefaultNetworkTimeOut(timeout):
	import socket
	socket.setdefaulttimeout(timeout)

snapshot = SZDIYPic() #initialize an instance
aWX = WX() #initialize a WX instance, this will request a new accesstoken
setDefaultNetworkTimeOut(30) #set network timeout

while True:

	#takeAShot(name,width,height):
	snapshot.takeAShot('image.jpg',800,600)
	snapshot.compressImageAndApplyWaterMark ('image.jpg', 'new.jpg', quality=80, fontSize=14, hLocation=5, vLocation=5)
	media_id,created_at = aWX.uploadToWx('new.jpg',TMPDIRECTORY) #upload new picture to weixin
	uploadAFileToLinodeWithWXMediaID(TMPDIRECTORY+'/'+'new.jpg', media_id, created_at) #upload new pic to REST API picture server and notify it with weixin picture id at the same time.
	time.sleep(1)
	
	snapshot.takeAShot('image.jpg',1600,1200)
	snapshot.compressImageAndApplyWaterMark('image.jpg','new.jpg', quality=95, enWaterMark=False)
	snapshot.storeImg('new.jpg', TMPDIRECTORY) #this saves the image after compressing but without watermark
	snapshot.compressImageAndApplyWaterMark('image.jpg','new.jpg', quality=95, fontSize=27, hLocation=10, vLocation=10)
	uploadingAFileToQiNiu('szdiy','new.jpg',TMPDIRECTORY)

	time.sleep(20)


