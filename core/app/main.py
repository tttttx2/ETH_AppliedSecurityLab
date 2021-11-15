from flask import Flask
from flask import request
from flask import send_file
import jwt
import time

import base64
import os
import hashlib
import json
app = Flask(__name__)

@app.route("/")
def route_hello():
    return "Hello World from Flask"

@app.route("/login", methods=['POST'])
def route_login_user():
    email = request.form.get('email')
    passwd = request.form.get('passwd')
    
    #TODO check that with DB
    login = True
    
    if(login):
        token = gen_token(email) #yes, we're using direct email input here, not parsed
        return token, 200
    return "AUTH FAILED", 403

@app.route("/verify_cert", methods=['POST'])
def route_verify_cert():
    #TODO
    return "cert valid"

@app.route("/revoke_cert", methods=['POST'])
def route_revoke_cert():
    token = request.form.get('token')
    if(not checkauth(token)):
        log(request.path, request.data)
        return "Auth failed", 403
    email_parsed = parse_email(token)

    status = revoke_certificate(email_parsed)    
    if (status):
        log(request.path, "***CERT REVOKED***")
        return "cert revoked", 200
    log(request.path, request.data)
    return "ERROR: REVOKATION FAILED.", 403

@app.route("/create_cert", methods=['POST'])
def route_create_cert():
    token = request.form.get('token')
    if(not checkauth(token)):
        log(request.path, request.data)
        return "Auth failed", 403
    email_parsed = parse_email(token)
    
    status = create_certificate(email_parsed)
    if (status):
        log(request.path, "***CERT GENERATED***")
        return "cert created", 200
    log(request.path, request.data)
    return "ERROR: GENERATION FAILED.", 403

@app.route("/get_cert", methods=['POST'])
def route_get_cert():
    token = request.form.get('token')
    if(not checkauth(token)):
        log(request.path, request.data)
        return "Auth failed", 403
    email_parsed = parse_email(token)
    
    sernr=get_sernr_from_email(email_parsed)
    if(sernr == False):
        print("ERROR downloading certificate!")
        log(request.path, request.data)
        return 'ERROR downloading certificate', 403
    log(request.path, "***CERT DOWNLOADED***")
    return send_file('/data/issued/'+sernr+'.pfx', as_attachment=True), 200
    
    return "ERROR GENERATING CRL", 403

@app.route("/admin", methods=['POST'])
def route_admin():
    #TODO: login token somehow. As it's readonly not much security is needed?
    total_issued = 0
    total_valid = 0
    total_revoked = 0
    current_sernr = 0
    with open('/data/index.txt', 'r') as read_obj:
        for line in read_obj:
            line = line.split()
            if line[0]=="V":
                total_valid += 1
            if line[0]=="R":
                total_revoked += 1
            total_issued += 1
    with open('/data/srlnumber', 'r') as read_obj:
        for line in read_obj:
            current_sernr = line.strip()
    return json.dumps({"issued":total_issued, "revoked":total_revoked, "valid": total_valid, "serial":current_sernr})

@app.route("/generate_crl") #should be called from main landingpage webserver periodically to publish newest CRL
def route_generate_crl():
    returncode = os.system('openssl ca -config /etc/ssl/openssl.cnf -gencrl -out /data/crl.pem -passin pass:'+os.getenv('CA_CERT_PASSWD'))
    if(returncode == 0):
        log(request.path, "***CRL GENERATED***")
        return send_file('/data/crl.pem', as_attachment=True), 200
    log(request.path, request.data)
    return "ERROR GENERATING CRL", 403

@app.route("/revokelist", methods=['POST']) # not really necessary but maybe handy for admin interface?
def route_revokelist():
    onlyfiles = [f for f in os.listdir('/data/revoked') if os.path.isfile(os.path.join('/data/revoked', f))]
    return json.dumps(onlyfiles)

@app.route("/get_pubca") #should be called from main landingpage webserver with low periodicity to publish newest CA public key
def route_get_pubca():
    return send_file('/data/myCA.pem', as_attachment=True)

@app.route("/reset_ca", methods=['GET'])
# TODO: DISABLE AFTER DEVELOPMENT!
def route_reset_ca():
    os.system('echo "00" > /data/sernumber')
    os.system('echo "00" > /data/crlnumber')
    os.system('echo -n "" > /data/index.txt')
    os.system('echo -n "" > /data/crl.pem')
    os.system('rm /data/newcerts/*')
    os.system('rm /data/issued/*')
    os.system('rm /data/revoked/*')
    os.system('rm /data/tmp/*')
    return "CA COMPLETELY CLEARED."

def gen_token(email):
    payload_data = {"email": email, "time": time.time()}
    token = jwt.encode(payload=payload_data, key=os.getenv('JWT_SECRET'))
    return token
    
def checkauth(token):
    try:
        jwt.decode(token, key=os.getenv('JWT_SECRET'), algorithms=['HS256', ])
        # TODO: see if too old
    except:
        return False
    return True

def parse_email(token):
    email = jwt.decode(token, key=os.getenv('JWT_SECRET'), algorithms=['HS256', ])["email"]
    email_parsed = email #TODO: filter strange email addresses like "asdf+comment@asdf.asdf and parse for secruity
    return email_parsed

def backup():
    #TODO: tar /data, encrypt and send to backup server
    os.system('tar -czf - /data/* | openssl enc -e -aes256 -out /root/backup.tar.gz -passout pass:'+os.getenv('CA_CERT_PASSWD'))
    # post request this to backup server
    return

def log(action, payload):
    if (payload):
        payload = base64.b64encode(payload.encode("utf-8"))
    else:
        payload = base64.b64encode("NO PAYLOAD LOGGED".encode("utf-8"))
    #TODO: send to logging server
    return

def get_sernr_from_email(email_parsed):
    with open('/data/index.txt', 'r') as read_obj:
        for line in read_obj:
            if email_parsed in line:
                line = line.split()
                if line[0]=="V":
                    sernr_to_revoke = line[2]
                    return sernr_to_revoke
    return False

def create_certificate(email_parsed):
    tmp_location = "/data/tmp/"
    email_md5 = hashlib.md5(email_parsed.encode('utf-8')).hexdigest()
    filename = tmp_location+email_md5
    
    returncode = 0
    
    returncode += os.system('openssl req -new -nodes -sha256 -newkey rsa:2048 -keyout '+filename+'.key -out '+filename+'.csr -subj "/emailAddress='+email_parsed+'/CN=imovies.ch/O=imovies email/OU=iMovies email/C=CH/ST=Zuerich/L=Zuerich"')
    returncode += os.system('openssl ca -batch -config /etc/ssl/openssl.cnf -extensions usr_cert -notext -md sha256 -in '+filename+'.csr -out '+filename+'.crt -passin pass:'+os.getenv('CA_CERT_PASSWD'))
    returncode += os.system('openssl pkcs12 -export -in '+filename+'.crt -inkey '+filename+'.key -out '+filename+'.pfx -passout pass:')
    
    sernr_generated=get_sernr_from_email(email_parsed)
    if(sernr_generated == False or returncode != 0):
        print("ERROR generating certificate!")
        return False
    os.system('mv '+filename+'.pfx /data/issued/'+sernr_generated+'.pfx')
    #os.system('mv '+filename+'.crt /data/issued/'+sernr_generated+'.crt')
    #os.system('mv '+filename+'.key /data/issued/'+sernr_generated+'.key')
    os.system('rm '+filename+'*')
    return True

def revoke_certificate(email_parsed):
   
    returncode = 0
   
    # get latest sernr from email
    sernr_to_revoke=get_sernr_from_email(email_parsed)
    if (sernr_to_revoke==False):
        print("ERROR revoking certificate! 1")
        return False
    
    returncode += os.system('mv /data/issued/'+sernr_to_revoke+'.pfx /data/revoked/')
    returncode += os.system('openssl ca -config /etc/ssl/openssl.cnf -revoke /data/newcerts/'+sernr_to_revoke+'.pem -passin pass:'+os.getenv('CA_CERT_PASSWD'))
    if (returncode != 0):
        print("ERROR revoking certificate! 2")
        return False
    return True

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
