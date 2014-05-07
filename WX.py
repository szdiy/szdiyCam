import requests
from credentials import wxAppID, wxAppSecret

urlEndPoint_AccessToken = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+wxAppID+'&secret='+wxAppSecret

class WX:
	def __init__(self):
		self.currentAccessToken = self.__getNewAccessToken() #at initialization, get a new access token

	def __getNewAccessToken(self):
		try:
			resp = requests.get(urlEndPoint_AccessToken)
			respJSON = resp.json()
			if 'access_token' in respJSON:
				print 'access_token: {}'.format(respJSON['access_token'])
				print 'expires in: {} sec'.format(respJSON['expires_in'])
				return respJSON['access_token']
			else:
				print respJSON
		except:
			print "get new access token network error"

	#refresh access token upon expire
	def refreshAccessToken(self):
		self.currentAccessToken = self.__getNewAccessToken()

	#upload a file to weixin
	def uploadToWx(self, image, directory):
		files={'files': open(directory+'/'+image, 'rb')}  
		try:
			r= requests.post(self.__getUrlEndpointForUpload(),files=files)
			# print r.json()
			if 'media_id' in r.json() and 'created_at' in r.json():
				print 'media_id: {}'.format(r.json()['media_id'])
				print 'created_at: {}'.format(r.json()['created_at'])
				return (r.json()['media_id'], r.json()['created_at'])
			elif 'errcode' in r.json():
				if r.json()['errcode'] in (40001, 40014, 41001, 42001, 42002, 40030, 41003): #those error token indicate expire of access token
					print ('old access token no longer work, get new access token')
					self.refreshAccessToken()
					print ('retry uploading')
					return self.uploadToWx(image,directory) #retry if fail
			else:
				print "unknown error: {}".format(r.json())
		except:
			print "upload network error"
	
	#weixin need to inject current access token into its upload url address
	def __getUrlEndpointForUpload(self):
		return 'http://file.api.weixin.qq.com/cgi-bin/media/upload?access_token='+self.currentAccessToken+'&type=image'
