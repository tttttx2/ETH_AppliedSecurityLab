from flask import Flask, render_template, redirect, url_for, request, make_response
from flask import send_file
from io import BytesIO
import os
import requests
import time
import json
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    status = None
    token = request.cookies.get('token')
    if token is not None:
        headers = {'X-SERVICE-NAME': os.getenv('SERVICE_NAME')}
        files = {'token': (None, token)}
        r = requests.post('https://10.0.0.10/get_info',headers=headers,files=files)
        if r.status_code is not 200:
            resp = make_response(redirect('/login'))
            resp.set_cookie('token', '', expires=0)
            return resp
        user_info = r.json()[0]
        if request.method == 'POST':
            if "create" in request.form:
                r = requests.post('https://10.0.0.10/create_cert',headers=headers,files=files)
                if r.status_code is not 200:
                    status = r.text
            elif "download" in request.form: 
                r = requests.post('https://10.0.0.10/get_cert',headers=headers,files=files)
                if r.status_code is not 200:
                    status = r.text
                else:
                    byte_io = BytesIO(r.content)
                    return send_file(byte_io, download_name='cert.pfx',as_attachment=True)
            elif "revoke" in request.form: 
                r = requests.post('https://10.0.0.10/revoke_cert',headers=headers,files=files)
                if r.status_code is not 200:
                    status = r.text
            elif "edit_info" in request.form: 
                if request.form['firstname'].strip() != user_info['firstname'] or \
                   request.form['lastname'].strip()  != user_info['lastname']:
                    print(request.form['firstname'].strip())
                    files = {
                        'token': (None, token),
                        'firstname': (None, request.form['firstname'].strip()),
                        'lastname': (None, request.form['lastname'].strip())
                    }
                    r = requests.post('https://10.0.0.10/edit_info',headers=headers,files=files)
                    return redirect(request.referrer)
            elif "logout" in request.form: 
                resp = make_response(redirect('/login'))
                resp.set_cookie('token', '', expires=0)
                return resp
            else: 
                print(request.form)
                status = 'Invalid Operation!'
        return render_template('index.html',status=status,user_info=user_info)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        headers = {'X-SERVICE-NAME': os.getenv('SERVICE_NAME')}
        files = {
            'uid': (None, request.form['uid']),
            'passwd': (None, request.form['passwd']),
        }
        r = requests.post('https://10.0.0.10/login',headers=headers,files=files)
        if r.status_code is not 200:
            error = r.text
        else:
            resp = make_response(redirect('/'))
            resp.set_cookie('token', r.text)
            return resp
    resp = make_response(render_template('login.html', error=error))
    resp.set_cookie('token', '', expires=0)
    return resp

@app.route('/admin', methods=['GET', 'POST'])
def login_admin():
    error = None
    if request.method == 'POST':
        headers = {'X-SERVICE-NAME': os.getenv('SERVICE_NAME')}
        files = {
            'admintoken': (None, request.form['passwd']),
        }
        r = requests.post('https://10.0.0.10/admin',headers=headers,files=files)
        if r.status_code is not 200:
            error = r.text
        else:
            resp = make_response(redirect('/admin/stats'))
            resp.set_cookie('admintoken', request.form['passwd'])
            return resp
    resp = make_response(render_template('adminlogin.html', error=error))
    resp.set_cookie('admintoken', '', expires=0)
    return resp

@app.route('/admin/stats', methods=['GET', 'POST'])
def stats_admin():
    if request.method == 'POST':
        resp = make_response(redirect('/admin'))
        resp.set_cookie('admintoken', '')
        return resp
    
    headers = {'X-SERVICE-NAME': os.getenv('SERVICE_NAME')}
    admintoken = request.cookies.get('admintoken')
    if not admintoken or admintoken == '':
        resp = make_response(redirect('/admin'))
        return resp
    print(admintoken)
    files = {
        'admintoken': (None, admintoken),
    }
    r = requests.post('https://10.0.0.10/admin',headers=headers,files=files)
    if r.status_code is not 200:
        resp = make_response(redirect('/admin'))
        return resp
    else:
        print(r.text)
        resp = make_response(render_template('adminstats.html', stats=json.loads(r.text)))
        return resp

@app.route('/crl', methods=['GET'])
def download_crl():
    path = '/crl.pem'
    exists = os.path.isfile(path)
    if not exists:
        r = requests.get('https://10.0.0.10/generate_crl', allow_redirects=True)
        open(path, 'wb').write(r.content)
        
    modifytime = os.path.getmtime(path)
    if time.time() - modifytime > 1000:
        r = requests.get('https://10.0.0.10/generate_crl', allow_redirects=True)
        open(path, 'wb').write(r.content)
        
    return send_file(path, as_attachment=True), 200

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
