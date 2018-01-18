# Main program for taking picture from camera, upload the picture to QiNiu,
# and upload the resource info to SDZIY server
from picture import SZDIYPic
from upload import setDefaultNetworkTimeOut
from upload.qiniu_uploader import uploadingAFileToQiNiu
from upload.update_server import updateImageInfo, getQiniuUpdateInfo
from config import IMAGE_PATH, SOCKET_TIMEOUT, SLEEP_PERIOD

# A daemon program for taking picture and uploading to server in every period
snapshot = SZDIYPic()
setDefaultNetworkTimeOut(SOCKET_TIMEOUT)

while True:

    # take a snapshot


    # save to a local archive


    # upload to qiniu


    # uploado to QiNiu (should be async?)


    # sleep period
    time.sleep(SLEEP_PERIOD or 20)
