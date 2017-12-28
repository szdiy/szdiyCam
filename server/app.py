# Server App:
#
# Provide APIs for:
# 1. RPi to update the latest screenshot
# 2. View the latest image
# 3. (next step) For admin to view all the images
#
from flask import Flask, g, request, redirect, make_response
from db import init_db, close_connection
from model import save_image_info, get_latest_screenshot
from qiniu_utils import getDownloadUrl
import json, traceback

app = Flask(__name__)
init_db( app )

@app.route('/')
def hello_world():
    return 'SZDIY Camera Server'

HTTP_MOVED_TEMPORARILY = 302
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_SERVER_ERROR = 500

# general error response data
def error_response(reason, code):
    ret = json.dumps({
        "error": code,
        "msg": reason
    })
    return make_response(ret, code)

# general successful resposne data
def success_resposne(data, code=200):
    ret = json.dumps({
        "data": data
    })

    return make_response(ret, code)

@app.route('/update', methods=['post'])
def screenshot_update():
    if not request.data:
        return error_response('Data empty', HTTP_BAD_REQUEST)

    info = None
    try:
        info = json.loads(request.data)
    except:
        return error_response('Data invalid', HTTP_BAD_REQUEST)

    # save image info
    try:
        save_image_info( info )
    except Exception as e:
        traceback.print_exc()
        return error_response('Save data error: {}'.format(e), HTTP_SERVER_ERROR)

    return success_resposne( { 'msg': 'OK' } )

@app.route("/screenshot/<deviceId>/latest", methods=['get'])
def screenshot_latest(deviceId):
    if not deviceId:
        return error_response('Device name empty', HTTP_BAD_REQUEST)

    screenshot = get_latest_screenshot( deviceId )
    if not screenshot:
        return error_response('Screenshot not found for the device: {}'.format( deviceId ),
            HTTP_NOT_FOUND)

    print( 'latest screenshot: {}'.format( screenshot ) )
    try:

        # can return json for debug information
        if request.args.get('format') == 'json':
            return success_resposne( screenshot )

        # return
        key = screenshot.get('image_key', '')
        if not key:
            return error_response('Image key not found in the record', HTTP_NOT_FOUND)
        download_link = getDownloadUrl( key )
        return redirect(download_link, code=HTTP_MOVED_TEMPORARILY)
    except Exception as e:
        traceback.print_exc()

    return error_response('Get image error', HTTP_MOVED_TEMPORARILY)





@app.teardown_appcontext
def teardown(exception):
    close_connection(exception)

# main method
if __name__ == '__main__':
    app.run(debug=True)
