# szdiyCam Setup for Raspberry Pi

### Setup environment

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

8. (Optional) A clear archive script is added for maintenance. You can add it to crontab so it can run once everyday.
		$ crontab -e
		0 0 * * * python /home/pi/szdiyCam/clearArchive.py 1>>/home/pi/szdiycam_cleararchive.log 2>> /home/pi/szdiycam_cleararchive.log &


### Setting System Service
