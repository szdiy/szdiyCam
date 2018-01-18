# Source Code Structure

Here are some notes for reading the source code.

## 1. Home

 * `/main.py`

 Main program for **szdiyCam**.

 * `/test.py`

 Just some testing script to prove the upload process.

## 2. /config

 * `./__init__.py`

 A few config items are provided here.

 * `./credentials.py`

 You should set tokens and sensitive information in this file according to _credentials.py.sample_.

## 3. /picture

 * `./PictureCamera.py`

 A wrapper class for taking picture from RPi camera.

 * `./SZDIYPic.py`

 An interface for taking picture and proceed necessary editing.

 **Note:** You can test the camera by running command `python -m picture.SZDIYPic`.

## 4. /upload

 * `./qiniu_uploader.py`

 Wrapper for Qiniu uploading interface.

 **Note:** You can test the qiniu upload by running command `python -m upload.qiniu_uploader`

 * `./linode.py`

 Wrapper for the interface uploading to SZDIY linode server.

## 4. /scripts

 * `./uploadingimage`

 A system start script to start up the daemon.

## 5. /archive

 * `./clearArchive.py`

 Auto archive the history images in the SD card on RPi.

## 6. /lib

 * `./WX.py`

 An intended but paused integration to Wechat.
