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

from credentials import QiNiuACCESS_KEY, QiNiuSECRET_KEY
import qiniu.conf
import qiniu.io
import sys
import qiniu.rs
import qiniu.io

def __upload(bucketName,fileName,localFilePath):
	qiniu.conf.ACCESS_KEY = QiNiuACCESS_KEY
	qiniu.conf.SECRET_KEY = QiNiuSECRET_KEY

	policy = qiniu.rs.PutPolicy(bucketName)
	policy.scope=bucketName+':'+unicode(fileName, "utf-8")
	uptoken = policy.token()

	extra = qiniu.io.PutExtra()
	extra.mime_type = "image/jpeg"
	f=open(localFilePath+'/'+fileName,'r')
	# localfile = "%s" % f.read()
	ret, err = qiniu.io.put(uptoken, fileName, f)
	f.close()
	print ret;
	if err is not None:
	    sys.stderr.write('error: %s ' % err)

def	uploadingAFileToQiNiu(bucket,fileName,localFilePath):
	print "uploading to qiniu"
	try:
		__upload(bucket,fileName,localFilePath)
	except:
		print "upload to QiNiu failed"