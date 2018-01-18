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

import os
import shutil
from datetime import datetime
from config import ARCHIVE_DATE

def date_diff(dateStr):
    try:
        now = datetime.now()
        d = datetime.strptime(dateStr, '%Y-%m-%d')
        return (now-d).days
    except: # catch all exception
        print("cannot parse:" + str(dateStr))
        return -1

def clear_archive(imgPath):
    print( 'cleaning files in archive path: {}'.format(imgPath))

    for folder in os.listdir(imgPath):
        if date_diff(folder) > ARCHIVE_DATE:
            shutil.rmtree(os.path.join(imgPath, folder))
            print("delete folder: " + str(folder))



if __name__ == '__main__':
    from config import IMAGE_PATH
    clear_archive( IMAGE_PATH )
