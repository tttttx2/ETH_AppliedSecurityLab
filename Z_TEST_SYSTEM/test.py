import requests, time, os
from datetime import datetime, timedelta

client = "https://client.imovies.ch"
admin = "https://client.imovies.ch/admin"
crl = "https://crl.imovies.ch"
logs= "https://logs.imovies.ch"



testwidth = 5
taskwidth = 50

def test_crl():
    # test if crl available
    status = True
    test = "CRL"
    
    task = "Download"
    r = requests.get(crl)
    if ("CRL" not in r.text):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    return status

def test_login():
    test = "LOGIN"
    status = True
    
    session = requests.Session()
    
    task = "wrong passwd"
    r = session.post(client+"/login", data={"uid":"test", "passwd":"THISISWRONG"})
    if ("AUTH FAILED" not in r.text):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    
    task = "correct passwd"
    r = session.post(client+"/login", data={"uid":"test", "passwd":"testtest"})
    if (not session.cookies.get_dict()['token']):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    #TODO: cert login
    
    task = "logout"
    r = session.get(client+"/login")
    if ("Login" not in r.text):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))

    
def cert_issuing():
    test = "CERT"
    session = requests.Session()
    r = session.post(client+"/login", data={"uid":"test", "passwd":"testtest"})
    if (session.cookies.get_dict().get('token') == '' or session.cookies.get_dict().get('token')==None):
        print("{} - {}: {}".format(test.ljust(testwidth), "LOGIN FAILED".ljust(taskwidth), str("SKIPPED UNIT").ljust(5)))
        return
    
    task = "create new cert"
    status=True
    r = session.post(client+"/", data={"create":"1"})
    if (r.status_code != 200):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    
    task = "create duplicate blocked"
    status=True
    r = session.post(client+"/", data={"create":"1"})
    if (r.status_code != 403):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    
    task = "download existing cert"
    status=True
    r = session.post(client+"/", data={"download":"1"})
    if (r.status_code != 200):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    
    task = "revoke existing cert"
    status=True
    r = session.post(client+"/", data={"revoke":"1"})
    if (r.status_code != 200):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))

    task = "revoke if no cert blocked"
    status=True
    r = session.post(client+"/", data={"revoke":"1"})
    if (r.status_code != 403):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))

    task = "download blocked if no cert"
    status=True
    r = session.post(client+"/", data={"download":"1"})
    if (r.status_code != 403):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))

    task = "edit info"
    status=True
    r = session.post(client+"/", data={"firstname":"NEW2", "lastname":"NEW1", "edit_info":"1"})
    session = requests.Session()
    r = session.post(client+"/login", data={"uid":"test", "passwd":"testtest"})
    if (session.cookies.get_dict().get('token') == None or session.cookies.get_dict().get('token')==''):
        status = False
    r = session.get(client+"/")
    if (( "NEW1" not in r.text or "NEW2" not in r.text)):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))

    task = "change passwd and logging in with new passwd"
    status=True
    r = session.post(client+"/edit_passwd", data={"passwd": "testtest", "new_passwd": "newpasswd", "confirm_new_passwd": "newpasswd"})
    session = requests.Session()
    r = session.post(client+"/login", data={"uid":"test", "passwd":"newpasswd"})
    if (session.cookies.get_dict().get('token') == None or session.cookies.get_dict().get('token')==''):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    
    task = "revert info back"
    status=True
    r = session.post(client+"/", data={"edit_info":"1", "firstname":"TEST", "lastname":"TEST"})
    r = session.post(client+"/login", data={"uid":"test", "passwd":"newpasswd"})
    r = session.get(client+"/")
    if (("TEST" not in r.text or "TEST" not in r.text or "test@imovies.ch" not in r.text)):
        status = False
    r = session.post(client+"/edit_passwd", data={"passwd": "newpasswd", "new_passwd": "testtest", "confirm_new_passwd": "testtest"})
    session = requests.Session()
    r = session.post(client+"/login", data={"uid":"test", "passwd":"testtest"})
    if (session.cookies.get_dict().get('token') == None or session.cookies.get_dict().get('token')==''):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    
    task = "logging in with reverted passwd"
    status=True
    session = requests.Session()
    r = session.post(client+"/login", data={"uid":"test", "passwd":"testtest"})
    if (session.cookies.get_dict().get('token') == None or session.cookies.get_dict().get('token')==''):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))

    
def test_admin():
    test = "ADMIN"
    task = "login"
    status=True
    session = requests.Session()
    r = session.post(client+"/admin", data={"uid":"admin", "passwd":"uoVei2phooZ3ateevahf"})
    if (session.cookies.get_dict().get('admintoken') == None or session.cookies.get_dict().get('admintoken')==''):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    
    task = "status page"
    status=True
    r = session.get(client+"/status")
    if ("issued" in r.text):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    
def test_logs():
    test = "LOGS"
    task = "login"
    status = True
    r = requests.get(logs, auth=("admin", "uoVei2phooZ3ateevahf"))
    if ("Index" not in r.text):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    
    task = "download log"
    status = True
    r = requests.get(logs+"/127.0.0.1/rsyslogd.log", auth=("admin", "uoVei2phooZ3ateevahf"))
    if (r.status_code != 200):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))

    task = "log running on 10.0.0.10 (past 1h)"
    status = True
    r = requests.get(logs+"/10.0.0.10/", auth=("admin", "uoVei2phooZ3ateevahf"))
    d = datetime.utcnow() - timedelta(hours=0)
    if (not (d.strftime("%d-%b-%Y %H") in r.text or d.strftime("%d-%b-%Y %H") in r.text)):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    
    task = "log running on 10.0.0.20 (past 1h)"
    status = True
    r = requests.get(logs+"/10.0.0.20/", auth=("admin", "uoVei2phooZ3ateevahf"))
    d = datetime.utcnow() - timedelta(hours=0)
    if (not (d.strftime("%d-%b-%Y %H") in r.text or d.strftime("%d-%b-%Y %H") in r.text)):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    
    task = "log running on 10.0.0.30 (past 1h)"
    status = True
    r = requests.get(logs+"/10.0.0.30/", auth=("admin", "uoVei2phooZ3ateevahf"))
    d = datetime.utcnow() - timedelta(hours=0)
    if (not (d.strftime("%d-%b-%Y %H") in r.text or d.strftime("%d-%b-%Y %H") in r.text)):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    
    task = "log running on 10.0.0.41 (past 1h)"
    status = True
    r = requests.get(logs+"/10.0.0.41/", auth=("admin", "uoVei2phooZ3ateevahf"))
    d = datetime.utcnow() - timedelta(hours=0)
    if (not (d.strftime("%d-%b-%Y %H") in r.text or d.strftime("%d-%b-%Y %H") in r.text)):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    
    task = "log running on 10.0.0.50 (past 1h)"
    status = True
    r = requests.get(logs+"/10.0.0.50/", auth=("admin", "uoVei2phooZ3ateevahf"))
    d = datetime.utcnow() - timedelta(hours=0)
    if (not (d.strftime("%d-%b-%Y %H") in r.text or d.strftime("%d-%b-%Y %H") in r.text)):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    
    task = "log running on 10.0.0.5 (past 1h)"
    status = True
    r = requests.get(logs+"/10.0.0.5/", auth=("admin", "uoVei2phooZ3ateevahf"))
    d = datetime.utcnow() - timedelta(hours=0)
    if (not (d.strftime("%d-%b-%Y %H") in r.text or d.strftime("%d-%b-%Y %H") in r.text)):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))

def test_ssh():
    test = "SSH"
    print("{} - {}: {}".format(test.ljust(testwidth), "NO TASKS".ljust(taskwidth), str("SKIPPED UNIT").ljust(5)))
    
def test_net():
    test = "NET"
    task = "ping VM 00 successful (DNS)"
    status = True
    r = os.system("ping imovies.ch -c 1 -w 5000 &> /dev/null")
    if (r!=0):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    
    task = "ping VM 00 successful (IP)"
    status = True
    r = os.system("ping 10.0.1.5 -c 1 -w 5000 &> /dev/null")
    if (r!=0):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    
    task = "ping VM 00 internal blocked"
    status = True
    r = os.system("ping 10.0.0.5 -c 1 -w 5000 &> /dev/null")
    if (r==0):
        status = False
    print("{} - {}: {}".format(test.ljust(testwidth), task.ljust(taskwidth), str(status).ljust(5)))
    
test_crl()
test_login()
cert_issuing()
test_admin()
test_logs()
test_ssh()
test_net()
