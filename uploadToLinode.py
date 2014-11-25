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
import requests
from credentials import LinodeServerImageUploadAPIURL, SZDIYCamAPIBaseURL

def __upload(files):
	print "uploading image to linode"
	requests.post(LinodeServerImageUploadAPIURL,files=files, timeout=20) #set time out at 20 secs
	print "image upload complete"

def uploadAFileToLinode(fileLocation):
	aFile = open(fileLocation,'rb')
	files = {'file': aFile}
	try:
		__upload(files)
	except:
		print "Network seems down, try again later..."
	aFile.close();

def uploadAFileToLinodeWithWXMediaID(fileLocation, media_id, created_at):
	print "uploading image to linode"
	aFile = open(fileLocation,'rb')
	files = {'file': aFile}
	
	try:
		postAddress = SZDIYCamAPIBaseURL+'/'+str(media_id)+'/'+str(created_at)+'/upload'
		r = requests.post(postAddress,files=files, timeout=20) #set time out at 20 secs
		print r
	except:
		print "Network seems down, try again later..."
	aFile.close();

