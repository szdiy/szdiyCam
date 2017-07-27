from upload.linode import uploadAFileToLinodeWithWXMediaID, uploadAFileToLinode

TMPDIRECTORY = '/tmp'
uploadAFileToLinodeWithWXMediaID(TMPDIRECTORY+'/'+'new.jpg', -1, -1) #upload new pic to REST API picture server and notify it with weixin picture id at the same time.
# uploadAFileToLinode(TMPDIRECTORY+'/'+'new.jpg')
