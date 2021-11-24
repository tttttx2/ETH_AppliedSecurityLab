from flask import Flask, request, redirect, url_for
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
        file = request.files['file']
        service = request.headers['X-SERVICE-NAME']
        if service not in allowed_services:
            return "service not whitelisted", 403
        if file.filename == '':
            print('No selected file')
            return "failed", 403
        if file:
            filename = secure_filename(service+"_"+str(int(time.time()))+".tar.gz.enc")#file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "upload done", 200 #redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload backup File</title>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=False, port=80)
