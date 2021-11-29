from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import time
import os
import base64
import requests


UPLOAD_FOLDER = '/data'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return True

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    allowed_services = ["core", "web", "log"]
    if request.method == 'POST':
        file = request.files['file']
        service = request.headers['X-SERVICE-NAME']
        if service not in allowed_services:
            log("", service+" backup: not whitelisted", "AUTH")
            return "service not whitelisted", 403
        if file.filename == '':
            print('No selected file')
            log("", service+" backup: no data received", "ERROR")
            return "failed", 403
        if file:
            filename = secure_filename(service+"_"+str(int(time.time()))+".tar.gz.enc")#file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            log("", service+" backup: done")
            return "upload done", 200 #redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload backup File</title>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def log(action, payload, level="INFO"):
    
    if (payload):
        payload = payload.encode("utf-8")
    else:
        payload = "NO PAYLOAD LOGGED".encode("utf-8")
    
    file_object = open('/var/log/application.log', 'a')
    file_object.write(str(level) + " - " + str(payload) + "\n\r")
    file_object.close()
    return

    #if (payload):
        #payload = base64.b64encode(payload.encode("utf-8"))
    #else:
        #payload = base64.b64encode("NO PAYLOAD LOGGED".encode("utf-8"))
    #headers = {'X-SERVICE-NAME': os.getenv('SERVICE_NAME')}
    #r = requests.post('https://10.0.0.40/', data={'logdata':payload, 'level':level}, headers=headers)
    #return

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=False, port=80)
