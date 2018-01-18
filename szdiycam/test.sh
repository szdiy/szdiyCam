#!/bin/bash

# ~~ A test program for testing and debugging the environment ~~
echo 'Test Program for SZDIY Cam'

# Taking picture from Camera
echo -e '>>> Test: taking picture from Camera'
python -m picture.SZDIYPic

# Testing Qiniu Upload
echo -e '\n>>> Test: uploading to Qiniu Storage'
python -m upload.qiniu_uploader

# Testing update to SZDIY server
echo -e '\n>>> Test: update info to SZDIY server'
python -m upload.update_server

# test clear archive
echo -n '\n>>> Test: clear archive job'
python -m archive.clearArchive
