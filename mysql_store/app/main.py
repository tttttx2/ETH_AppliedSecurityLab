from flask import Flask, request, redirect, url_for
from flask import send_file
from werkzeug.utils import secure_filename
import time
import os
import requests


app = Flask(__name__)

@app.route('/backup', methods=['GET'])
def view_backup():
    backup()
    return "backup triggered", 200

def backup():
    os.system('mysqldump -u '+os.getenv('MYSQL_USER')+' -p'+os.getenv('MYSQL_PASS')+' -h 10.0.0.30 db > /dump.sql')
    os.system('tar -czf - /dump.sql | openssl enc -e -aes256 -out /root/backup.tar.gz.enc -pass pass:'+os.getenv('BACKUP_PASSWD'))
    files = {'file': open('/root/backup.tar.gz.enc', 'rb')}
    headers = {'X-SERVICE-NAME': os.getenv('SERVICE_NAME')}
    r = requests.post('https://10.0.0.50/', files=files, headers=headers)        
    return

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=False, port=80)
