import requests
import datetime
from credentials import wxAppID, wxAppSecret

urlEndPoint_AccessToken = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+wxAppID+'&secret='+wxAppSecret

class WX:
	def __init__(self):
		self.currentAccessToken = self.__getNewAccessToken() #at initialization, get a new access token
		self.lastUploadTime = datetime.datetime.now() #keeps track of last upload time
		self.lastMedia_id = -1 #keeps track of last successful upload media_id
		self.lastCreated_at = -1 #keeps track of last successful upload created_at

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

	"""
	upload a file to weixin, private function
	return (media_id, created_at)
	return (-1,-1) upon exception
	
	"""
	def __uploadToWx(self, image, directory):
		files={'files': open(directory+'/'+image, 'rb')}  
		try:
			r= requests.post(self.__getUrlEndpointForUpload(),files=files)
			# print r.json()
			if 'media_id' in r.json() and 'created_at' in r.json():
				print 'media_id: {} | created_at: {}'.format(r.json()['media_id'], r.json()['created_at'])
				return (r.json()['media_id'], r.json()['created_at'])
			elif 'errcode' in r.json():
				if r.json()['errcode'] in (40001, 40014, 41001, 42001, 42002, 40030, 41003): #those error token indicate expire of access token
					print ('old access token no longer work, get new access token')
					self.refreshAccessToken()
					print ('retry uploading')
					return self.__uploadToWx(image,directory) #retry if access token is expired
				else: #handling unknown error code
					print 'error code: {} | {}'.format(r.json()['errcode'],r.json()['errmsg'])
					raise ValueError
			else:
				print "unknown error"
				raise ValueError
		except ValueError:
			return (-1,-1)
		except:
			print "upload network error"
			return (-1,-1)
	
	"""
	upload a file to weixin with api rate limiting
	return (media_id, created_at)
	return last successful media_id and created_at on error
	
	:type numbersPerDay: int
	:param numbersPerDay: limit api call to x times per day
	:type image: str
	:param image: image name such as new.jpg
	:type directory: str
	:param directory: directory location such as /tmp

	"""
	def uploadToWxWithAPICallLimit(self, numbersPerDay, image, directory):
		try:
			oncePerHowManySeconds = 24*3600/numbersPerDay #calcuate the execution frequency 'once per x seconds'
		except:
			print "numbersPerDay cannot be 0, set to default upload"
			media_id,created_at  = self.__uploadToWx(image,directory)
			self.lastMedia_id = media_id
			self.lastCreated_at = created_at
			return (media_id, created_at)

		currentTime = datetime.datetime.now()
		pastTime = self.lastUploadTime
		timeDiff = (currentTime - pastTime).total_seconds()

		if timeDiff > oncePerHowManySeconds:
			media_id,created_at  = self.__uploadToWx(image,directory)
			self.lastMedia_id = media_id
			self.lastCreated_at = created_at
			self.lastUploadTime = currentTime #update upload time
		else:
			print 'last upload to WX happened {} seconds ago, less than {} seconds required to meet the API limit for {} times per day'.format(timeDiff, oncePerHowManySeconds, numbersPerDay)
			print 'media_id: {} | created_at: {}'.format(self.lastMedia_id, self.lastCreated_at)
		
		return (self.lastMedia_id, self.lastCreated_at)

	#weixin need to inject current access token into its upload url address
	def __getUrlEndpointForUpload(self):
		return 'http://file.api.weixin.qq.com/cgi-bin/media/upload?access_token='+self.currentAccessToken+'&type=image'
