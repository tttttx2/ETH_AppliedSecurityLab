from flask import Flask, request, redirect, url_for
from flask import send_file
from werkzeug.utils import secure_filename
import time
import os


UPLOAD_FOLDER = '/data'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return True

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    allowed_services = ["core", "web", "log"]
    if request.method == 'POST':
        logdata = request.form.get('logdata')
        service = request.headers['X-SERVICE-NAME']
        if service not in allowed_services:
            return "service not whitelisted", 403
        if logdata == '':
            print('No logdata')
            return "failed", 403
        filename = secure_filename(service+".log")#file.filename)
        file_object = open(UPLOAD_FOLDER+"/"+filename, 'a')
        file_object.write('{time:"'+str(float(time.time()))+'", service:"'+service+'" ,data:"'+logdata+'"}\n')
        file_object.close()
        return "log done", 200 #redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload backup File</title>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
    
@app.route('/view/<service>', methods=['GET'])
def view_file(service):
    allowed_services = ["core", "web", "backup"]
    if service not in allowed_services:
        return "service not whitelisted", 403
    filename = UPLOAD_FOLDER+"/"+secure_filename(service+".log")#file.filename)
    return send_file(filename, as_attachment=False), 200

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=False, port=80)
