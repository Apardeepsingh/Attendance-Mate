import pymysql

def connect():
    conn = pymysql.connect(host='localhost', database="faceattendancesystem", user="root",  password="Sunnysingh@7689")

    return conn


def verifyEmail(mail):
    if '@' in mail and '.' in mail:
        return 'Valid'
    else:
        return 'Invalid'
    

def verifyMobile(mobile):
    if len(mobile) == 10 and mobile.isdigit():
        if mobile[0] in '6789':
            return 'Valid'
        else:
            return 'Invalid'
    else:
        return 'Invalid'