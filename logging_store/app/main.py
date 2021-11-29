from flask import Flask, request, redirect, url_for
from flask import send_file
from werkzeug.utils import secure_filename
import time
import os
import requests


app = Flask(__name__)


#UPLOAD_FOLDER = '/data'

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#def allowed_file(filename):
    #return True

#@app.route('/', methods=['GET', 'POST'])
#def upload_file():
    #allowed_services = ["core", "web", "backup"]
    #if request.method == 'POST':
        #logdata = request.form.get('logdata')
        #level= request.form.get('level')
        #service = request.headers['X-SERVICE-NAME']
        #if service not in allowed_services:
            #return "service not whitelisted", 403
        #if logdata == '':
            #print('No logdata')
            #return "failed", 403
        #filename = secure_filename(service+".log")#file.filename)
        #file_object = open(UPLOAD_FOLDER+"/"+filename, 'a')
        #file_object.write('{time:"'+str(float(time.time()))+'", service:"'+service+'", level:"'+level+'", data:"'+logdata+'"}\n')
        #file_object.close()
        #return "log done", 200 #redirect(url_for('download_file', name=filename))
    #return '''THE LOG STORAGE THINGY tm'''
    
#@app.route('/view/<service>', methods=['GET'])
#def view_file(service):
    #allowed_services = ["core", "web", "backup"]
    #if service not in allowed_services:
        #return "service not whitelisted", 403
    #filename = UPLOAD_FOLDER+"/"+secure_filename(service+".log")#file.filename)
    #return send_file(filename, as_attachment=False), 200

@app.route('/backup', methods=['GET'])
def view_backup():
    backup()
    return "backup triggered", 200

def backup():
    os.system('tar -czf - /data/* | openssl enc -e -aes256 -out /root/backup.tar.gz.enc -pass pass:'+os.getenv('BACKUP_PASSWD'))
    files = {'file': open('/root/backup.tar.gz.enc', 'rb')}
    headers = {'X-SERVICE-NAME': os.getenv('SERVICE_NAME')}
    r = requests.post('https://10.0.0.50/', files=files, headers=headers)        
    return

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=False, port=80)
