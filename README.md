#szdiyCam

szdiyCam project is ran on top of a [Raspberry Pi](www.raspberrypi.org/‎) with its [camera board](www.raspberrypi.org/tag/camera-board/‎). It takes a picture every 20sec and upload it to a custom image API server and [QiNiu](qiniu.com). The pictures taken are stored away in a local folder for later retrieval. The project is community project by [SZDIY Hackers' Community](http://www.szdiy.org/).

##Default Directory
The default directory can be changed inside `config.py`

1. `/tmp` for temporary picture storage before moving to a storage location
2. `/home/pi/szdiy_img` stores every pictures taken. They are sorted by date into different folders under it

##Setup
1. Clone the project

		cd szdiyCam
		
2. Setup virtual environment to insure anything you did inside the directory does not pollute your system

		virtualenv venv
		
3. Activate virtualenv

		source venv/bin/activate
	
4. Install dependencies using pip

		pip install -r requirements.txt 

5. If you already install PIL in your system, and step 3 failed, manually link your PIL library inside virtualenv directory

		ln -s /usr/local/lib/python2.7/dist-packages/PIL* venv/lib/python2.7/site-packages/
		
6. copy `credentials.py.sample` to `credentials.py`. You will need to arrange your own picture API server there. The sample used [QiNiu](qiniu.com) and a custom written API image server backend which is not part of this project. But it can be easily extended for other image uploading service such as [Imagur API](https://api.imgur.com)

7. If you get a [QiNiu](qiniu.com) API key successfully, you can now run without any issues

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
Apache License V3
	
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