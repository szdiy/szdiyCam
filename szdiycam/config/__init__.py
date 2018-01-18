# Copyright (C) 2014 SZDIY Hackers' Community
#
# This file is part of szdiyCam.
#
# szdiyCam is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# szdiyCam is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with szdiyCam.  If not, see <http://www.gnu.org/licenses/>.

TMPDIRECTORY  = '/tmp'
TMPIMAGE = 'image.jpg'
IMAGE_PATH = '/home/pi/szdiy_img'
ARCHIVE_DATE = 7
SOCKET_TIMEOUT = 30 # 30sec
SLEEP_PERIOD = 20 # 20sec per snapshot at least

# WX plugin
WXAPIUploadLimitPerDay = 500 #set the limit of api call per day for wechat

# Qiniu plugin
QiNiuImageExpiresTime = 3600
