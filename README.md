#szdiyCam

szdiyCam project runs on top of a [Raspberry Pi](www.raspberrypi.org/‎) with its [camera board](www.raspberrypi.org/tag/camera-board/‎). It takes a picture every 20sec and uploads it to a custom image API server and [QiNiu](qiniu.com). The pictures taken are stored away in a local folder for later retrieval. The project is a community project by [SZDIY Hackers' Community](http://www.szdiy.org/).

##Default Directory
The default directory can be changed in `config.py`

1. `/tmp` for temporary picture storage before moving to a archive location
2. `/home/pi/szdiy_img` stores every pictures taken. They are sorted by date into different folders.

##Setup
1. Clone the project

		cd szdiyCam
		
2. Setup virtual environment to ensure anything you did inside the directory does not pollute OS

		virtualenv venv
		
3. Activate virtualenv

		source venv/bin/activate
	
4. Install dependencies using pip

		pip install -r requirements.txt 

5. (optional) EXIF support
	* Install `pyexiv2` which is used to make sure `exif` data is copied over correctly

			sudo apt-get install python-pyexiv2        
	* Link the `pyexiv2` library to virtual environment
		
			ln -s /usr/lib/python2.7/dist-packages/libexiv2python.so venv/lib/python2.7/site-packages/
			ln -s /usr/lib/python2.7/dist-packages/pyexiv2 venv/lib/python2.7/site-packages/
6. copy `credentials.py.sample` to `credentials.py`. You will need to arrange your own picture API server there. The sample used [QiNiu](qiniu.com) and a custom written API image server backend which is not part of this project. But it can be easily extended for other image uploading service such as [Imagur API](https://api.imgur.com) by creating your own uploading functions.

7. If you get a [QiNiu](qiniu.com) API key successfully setup in step 6, you can now run without any issues

		python main.py

###Setup as System Service
1. put `uploadingimage` under ```/etc/init.d/uploadingimage```
2. Make it executable

		sudo chmod +x uploadingimage
		
3. Make it run at startup

		update-rc.d uploadingimage defaults

4. For debugging purpose, you can reconnect this session by running

		sudo screen -r 'uploading image'

#License
GPL V3
	
	Copyright (C) 2014 SZDIY Hackers' Community

	szdiyCam is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	szdiyCam is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with szdiyCam.  If not, see <http://www.gnu.org/licenses/>.