from conf import QiNiuImageExpiresTime
from conf.credentials import QiNiuACCESS_KEY, QiNiuSECRET_KEY, QiNiuHost, QiNiuIsPrivateBucket
import qiniu
import os

def __getQiniu():
	return qiniu.Auth(QiNiuACCESS_KEY, QiNiuSECRET_KEY)

# Get file download url
def getDownloadUrl(fileName, isPrivate=QiNiuIsPrivateBucket):
	url = os.path.join(QiNiuHost, fileName)
	if not isPrivate: # if qiniu space is public
		return url
	else: # if qiniu space is private
		q = __getQiniu()
		return q.private_download_url(url, expires=QiNiuImageExpiresTime)
