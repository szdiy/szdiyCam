import os
import shutil
from datetime import datetime
from config import IMAGE_PATH, ARCHIVE_DATE

def date_diff(dateStr):
    try:
        now = datetime.now()
        d = datetime.strptime(dateStr, '%Y-%m-%d')
        return (now-d).days
    except: # catch all exception
        print("cannot parse:" + str(dateStr))
        return -1

def clear_archive():
    for folder in os.listdir(ARCHIVE_PATH):
        if date_diff(folder) > ARCHIVE_DATE:
            shutil.rmtree(os.path.join(ARCHIVE_PATH, folder))
            print("delete folder: " + str(folder))



if __name__ == '__main__':
    clear_archive()
