from db import get_db
from datetime import datetime

IMAGE_TYPE_QINIU = 'qiniu'

def save_qiniu_image_info(info):
    device = info.get('device', 'defaut') # device id
    time = datetime.now() # image update time
    hash = info.get('hash', None)
    key = info.get('key', None)

    if not hash or not key:
        raise RuntimeError('hash or key is missing for image info')

    # save image to database
    db = get_db()
    c = db.cursor()
    # check if device exists
    c.execute("SELECT * FROM device WHERE device_id=?", [device])
    if not c:
        raise RuntimeError('device not found!')

    # insert into screenshot
    c.execute("INSERT INTO screenshot VALUES (?,?,?,?,?)",
        [device, time, IMAGE_TYPE_QINIU, hash, key])

    db.commit()

# common interface for saving image info
def save_image_info(info):
    if info["type"] == IMAGE_TYPE_QINIU:
        save_qiniu_image_info(info)
    else:
        pass

def get_latest_screenshot( deviceId ):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM screenshot WHERE device_id=? ORDER BY time DESC",
        [ deviceId ])
    return c.fetchone()
