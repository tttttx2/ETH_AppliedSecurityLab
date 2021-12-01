from abc import get_cache_token
from flask import Flask
from flask import request
from flask import send_file
from urllib import parse
import jwt
import time
import hashlib
import re

import base64
import os
import hashlib
import json
app = Flask(__name__)
import mysql.connector
import requests

mydb = mysql.connector.connect(
  host="10.0.0.30",
  user=os.getenv('MYSQL_USER'),
  password=os.getenv('MYSQL_PASS'),
  database="db"
)


@app.route("/")
def route_hello():
    apihint = """
Production:
    POST /login             (uid, passwd)
    POST /get_info          (token)
    POST /verify_cert       (cert)
    POST /revoke_cert       (token)
    POST /create_cert       (token)
    POST /get_cert          (token)
    POST /admin             (token)
    GET /generate_crl       (NONE)
    GET /get_pubca          (NONE)
    GET /revokelist         (NONE)
Development:
    GET /reset_ca           (NONE)
    GET /backup             (NONE)
    """
    
    return "You reached core.\n"+apihint


@app.route("/login", methods=['POST'])
def route_login_user():
    uid = request.form.get('uid')
    passwd = request.form.get('passwd')
    passwd_sha1 = hashlib.sha1(passwd.encode("UTF-8")).hexdigest()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT email FROM users WHERE uid=%s AND pwd=%s" , (uid, passwd_sha1,))

    myresult = mycursor.fetchall()
    
    login = (len(myresult) == 1)
    if(login):
        email = myresult[0][0]
        print(email)
        token = gen_token(email) #yes, we're using direct email input here, not parsed
        log(request.path, "AUTH SUCCESSFUL: "+email, "AUTH")
        return token, 200
    log(request.path, "AUTH FAILED: "+uid, "AUTH")
    return "AUTH FAILED", 403

@app.route("/edit_info", methods=['POST'])
def route_edit_info():
    token = request.form.get('token')
    if(not checkauth(token)):
        log(request.path, request.data, "AUTH")
        return "Auth failed", 403
    email_parsed = parse_email(token)

    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = parse_email_raw(request.form.get('email'))
    if (email==False):
        return "Email security check failed", 403

    mycursor = mydb.cursor()

    mycursor.execute("UPDATE users SET firstname=%s, lastname=%s, email=%s WHERE email=%s" , (firstname, lastname, email, email_parsed, ))
    mydb.commit()
    if email != email_parsed:
        revoke_certificate(email_parsed)
    return "Edit info success", 200

@app.route("/edit_passwd", methods=['POST'])
def route_edit_passwd():
    token = request.form.get('token')
    if(not checkauth(token)):
        log(request.path, request.data, "AUTH")
        return "Auth failed", 403
    email_parsed = parse_email(token)

    passwd = request.form.get('passwd')
    passwd_sha1 = hashlib.sha1(passwd.encode("UTF-8")).hexdigest()

    mycursor = mydb.cursor()

    mycursor.execute("SELECT email FROM users WHERE email=%s AND pwd=%s" , (email_parsed, passwd_sha1,))

    myresult = mycursor.fetchall()
    
    login = (len(myresult) == 1)
    if login is False:
        log(request.path, "AUTH FAILED: "+email_parsed, "AUTH")
        return "AUTH FAILED", 403

    new_passwd = request.form.get('new_passwd')
    new_passwd_sha1 = hashlib.sha1(new_passwd.encode("UTF-8")).hexdigest()

    mycursor.execute("UPDATE users SET pwd=%s WHERE email=%s" , (new_passwd_sha1, email_parsed, ))
    mydb.commit()
    return "Edit password success", 200


@app.route("/get_info", methods=['POST'])
def route_get_info():
    token = request.form.get('token')
    if(not checkauth(token)):
        log(request.path, request.data, "AUTH")
        return "Auth failed", 403
    email_parsed = parse_email(token)
    mycursor = mydb.cursor()

    mycursor.execute("SELECT uid, lastname, firstname, email FROM users WHERE email=%s" , (email_parsed, ))
    row_headers=[x[0] for x in mycursor.description]
    myresult = mycursor.fetchall()
    #return str(myresult)
    json_data=[]
    for result in myresult:
        json_data.append(dict(zip(row_headers,result)))
    return json.dumps(json_data), 200

@app.route("/verify_cert", methods=['POST'])
def route_verify_cert():
    #TODO
    #return "cert valid"
    cert_enc = request.form.get('cert')

    # Client certificate in PEM format
    cert = parse.unquote(cert_enc)

    name = hashlib.md5(cert.encode('ascii')).hexdigest()

    # Check if certificate exsits locally,
    with open("/data/tmp/" + str(name), mode='w+') as f:
        f.write(cert)

    res = os.popen("openssl verify -verbose -CAfile /data/myCA.pem /data/tmp/"+str(name)).read()
    #return res
    if "OK" in res and not_revoked(cert):
        email = os.popen("openssl x509 -noout -in /data/tmp/"+str(name)+" -email").read()
        email = "".join(email.split())
        token = gen_token(email)
        return token

    else:
        log(request.path, request.data, "AUTH WITH CLIENT CERT FAILED")
        return res, 403
        

    #openssl x509 -noout -in client.pem -email

@app.route("/revoke_cert", methods=['POST'])
def route_revoke_cert():
    token = request.form.get('token')
    if(not checkauth(token)):
        log(request.path, request.data, "AUTH")
        return "Auth failed", 403
    email_parsed = parse_email(token)

    status = revoke_certificate(email_parsed)    
    if (status):
        log(request.path, "***CERT REVOKED***")
        return "cert revoked", 200
    log(request.path, request.data, "ERROR")
    return "ERROR: REVOKATION FAILED.", 403

@app.route("/create_cert", methods=['POST'])
def route_create_cert():
    token = request.form.get('token')
    if(not checkauth(token)):
        log(request.path, request.data, "AUTH")
        return "Auth failed", 403
    email_parsed = parse_email(token)
    
    status = create_certificate(email_parsed)
    if (status):
        log(request.path, "***CERT GENERATED***")
        return "cert created", 200
    log(request.path, request.data, "ERROR")
    return "ERROR: GENERATION FAILED.", 403

@app.route("/get_cert", methods=['POST'])
def route_get_cert():
    token = request.form.get('token')
    if(not checkauth(token)):
        log(request.path, request.data, "AUTH")
        return "Auth failed", 403
    email_parsed = parse_email(token)
    
    sernr=get_sernr_from_email(email_parsed)
    if(sernr == False):
        print("ERROR downloading certificate!")
        log(request.path, request.data, "ERROR")
        return 'ERROR downloading certificate', 403
    log(request.path, "***CERT DOWNLOADED***")
    with open('/data/issued/'+sernr+'.pfx', mode='rb') as file: # b is important -> binary
        fileContent = file.read()
    return fileContent, 200#send_file('/data/issued/'+sernr+'.pfx', as_attachment=True), 200
    
    return "ERROR GENERATING CRL", 403

@app.route("/admin", methods=['POST'])
def route_admin():
    #login token somehow. As it's readonly not much security is needed?
    token = request.form.get('admintoken')
    if (token != os.getenv('ADMIN_STATS_TOKEN')):
        return "AUTH FAILED", 403
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
    log(request.path, request.data, "ERROR")
    return "ERROR GENERATING CRL", 403

@app.route("/revokelist") # not really necessary but maybe handy for admin interface?
def route_revokelist():
    revokelist = {}
    for f in os.listdir('/data/revoked'):
        if os.path.isfile(os.path.join('/data/revoked', f)) and not f.startswith('.'):
            revokelist[f] = os.popen('openssl pkcs12 -in /data/revoked/'+f+' -passin pass: -clcerts -nokeys | openssl x509').read()
    return json.dumps(revokelist), 200

@app.route("/get_pubca") #should be called from main landingpage webserver with low periodicity to publish newest CA public key
def route_get_pubca():
    return send_file('/data/myCA.pem', as_attachment=True)

@app.route("/reset_ca", methods=['GET'])
# TODO: DISABLE AFTER DEVELOPMENT!
def route_reset_ca():
    log(request.path, "***RESETTING CA***")
    os.system('echo "00" > /data/sernumber')
    os.system('echo "00" > /data/crlnumber')
    os.system('echo -n "" > /data/index.txt')
    os.system('echo -n "" > /data/crl.pem')
    os.system('rm /data/newcerts/*')
    os.system('rm /data/issued/*')
    os.system('rm /data/revoked/*')
    os.system('rm /data/tmp/*')
    return "CA COMPLETELY CLEARED."

@app.route("/backup", methods=['GET'])
# TODO: DISABLE AFTER DEVELOPMENT!
def route_backup():
    backup()
    return "backup done", 200


def gen_token(email):
    payload_data = {"email": email, "time": time.time()}
    token = jwt.encode(payload=payload_data, key=os.getenv('JWT_SECRET'))
    return token
    
def checkauth(token):
    try:
        token = jwt.decode(token, key=os.getenv('JWT_SECRET'), algorithms=['HS256', ])
        if int(time.time()) - int(float(token["time"])) > 60*10: # token validity 10 minutes
            return False
    except:
        return False
    return True

def parse_email(token):
    email = jwt.decode(token, key=os.getenv('JWT_SECRET'), algorithms=['HS256', ])["email"]
    email_parsed = parse_email_raw(email)
    return email_parsed

def parse_email_raw(email):
    pattern = re.compile("^\w+@imovies.ch$")
    if pattern.match(email):
        return email
    else:
        return False

def backup():
    os.system('tar -czf - /data/* | openssl enc -e -aes256 -out /root/backup.tar.gz.enc -pass pass:'+os.getenv('BACKUP_PASSWD'))
    files = {'file': open('/root/backup.tar.gz.enc', 'rb')}
    headers = {'X-SERVICE-NAME': os.getenv('SERVICE_NAME')}
    r = requests.post('https://10.0.0.50/', files=files, headers=headers)        
    return

def log(action, payload, level="INFO"):
    
    if (payload):
        payload = payload.encode("utf-8")
    else:
        payload = "NO PAYLOAD LOGGED".encode("utf-8")
    
    file_object = open('/var/log/core.log', 'a')
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

def not_revoked(cert):
    return True

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=False, port=80)
