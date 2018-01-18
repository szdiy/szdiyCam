from config.credentials import SERVER_HOST
import requests, json

def updateImageInfo( updateInfo ):
    url = SERVER_HOST + '/update'

    print('Uploading image info to server: {}'.format(url))
    response = requests.post( url, json=updateInfo )
    print('Result:{}'.format( response.content ))

def getQiniuUpdateInfo( device, imageInfo ):
    return {
        'device': device,
        'type': 'qiniu',
        'key': imageInfo[ 'key' ],
        'hash': imageInfo[ 'hash' ]
    }

if __name__ == '__main__':
    with open('qiniu_upload.log', 'r') as f:
        lines = f.readlines()
        if lines:
            qiniuImage = json.loads(lines[-1])
            updateImageInfo( getQiniuUpdateInfo( 'default', qiniuImage ) )
