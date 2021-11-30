from flask import Flask, render_template, redirect, url_for, request, make_response
from flask import send_file
from io import BytesIO
import os
import requests
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    status = None
    token = request.cookies.get('token')
    if token is not None:
        print("token:",token)
        headers = {'X-SERVICE-NAME': os.getenv('SERVICE_NAME')}
        files = {'token': (None, token)}
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
            elif "logout" in request.form: 
                resp = make_response(redirect('/login'))
                resp.set_cookie('token', '', expires=0)
                return resp
            else:
                error = 'Invalid Operation!'
        return render_template('index.html',status=status)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    cert_enc = request.headers.get('X-SSL-CERT')

    # Check first if any certificate was provided
    if cert_enc:
        headers = {'X-SERVICE-NAME': os.getenv('SERVICE_NAME')}
        r = requests.post('https://10.0.0.10/verify_cert',headers=headers, data={'cert': 'cert_enc'})
        if r.status_code is 200:
           json_data = r.json()
           email = json_data[0]["email"]
           token = json_data[0]["token"]

           resp = make_response(redirect('/'))
           resp.set_cookie('token', token)
           return resp
        error = r.text


    elif request.method == 'POST':
        headers = {'X-SERVICE-NAME': os.getenv('SERVICE_NAME')}
        files = {
            'email': (None, request.form['email']),
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

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
