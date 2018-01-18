# The MIT License (MIT)
#
# Copyright (c) 2013 QiNiu
# Modified from https://github.com/paulshi/qiniu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from config import TMPDIRECTORY, TMPIMAGE, QiNiuImageExpiresTime
from config.credentials import QiNiuACCESS_KEY, QiNiuSECRET_KEY, QiNiuBucketName, QiNiuHost, QiNiuIsPrivateBucket
import qiniu
import sys, os, traceback, json



def __getQiniu():
	return qiniu.Auth(QiNiuACCESS_KEY, QiNiuSECRET_KEY)

def __upload(bucketName,fileName,localFilePath):
	q = __getQiniu()

	# check file exist
	bucket = qiniu.BucketManager(q)
	ret, info = bucket.stat( bucketName, fileName )
	if ret:
		print('file key already exist: {}. delete it.'.format(fileName))
		# must delete it before upload it
		bucket.delete( bucketName, fileName )

	token = q.upload_token(bucketName)
	ret, info = qiniu.put_file(token, fileName, os.path.join(localFilePath, fileName))
	print('upload result: \nret: {}\n info: {}'.format(ret, info))

	return ret

def __logQiniuUpload( ret ):
	qiniuLogFile = 'qiniu_upload.log'
	if ret:
		with open(qiniuLogFile, 'a') as logger:
			logger.write( '{}{}'.format(json.dumps( ret ), os.linesep) )

# Upload a local file to Qiniu
def	uploadingAFileToQiNiu(fileName,localFilePath):
	print "uploading to qiniu"
	try:
		ret = __upload(QiNiuBucketName,fileName,localFilePath)
		__logQiniuUpload( ret )
		return ret
	except:
		print "upload to QiNiu failed"
		print traceback.format_exc()

# Get file download url
def getDownloadUrl(fileName, isPrivate=False):
	url = os.path.join(QiNiuHost, fileName)
	if not isPrivate: # if qiniu space is public
		return url
	else: # if qiniu space is private
		q = __getQiniu()
		return q.private_download_url(url, expires=QiNiuImageExpiresTime)


# Test Program to upload the temp captured file to Qiniu
if __name__ == '__main__':
	# Command line:
	# $ python -m upload.qiniu_uploader
	tmpfile = os.path.join(TMPDIRECTORY, TMPIMAGE)
	if not os.path.exists(tmpfile):
		print("Test image file not exist. Run camera test first!")

	result = uploadingAFileToQiNiu('image.jpg', TMPDIRECTORY)
	imageUrl = getDownloadUrl(result["key"], QiNiuIsPrivateBucket)
	print('Image url: {}'.format(imageUrl))
