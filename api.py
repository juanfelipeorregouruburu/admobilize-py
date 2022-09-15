import requests
import traceback
from datetime import datetime
from pytz import timezone
import csv
from urllib.request import urlopen
from bd import dbconnection

fmt = "%Y-%m-%d %H:%M:%S"
zona = 'America/Bogota'

def date_time():
    time_dt = datetime.now(timezone(zona))
    time_str = time_dt.strftime(fmt)
    time_str = (time_str.replace(' ','T'))+'-05:00'
    return time_str

def get_last_date_crowd():
    try:
        dbconn = dbconnection()
        mycursor = dbconn.cursor()
        sql = "SELECT date_time FROM crowd ORDER BY date_time DESC LIMIT 1"
        mycursor.execute(sql)
        dbconn.commit() 
        row = mycursor.fetchone()[0]
        row = (row.replace(' ','T'))+'-05:00'
        return row
    except:
        return '2022-01-01T00:00:00-05:00'

def get_last_date_aud():
    try:
        dbconn = dbconnection()
        mycursor = dbconn.cursor()
        sql = "SELECT date_time FROM audience ORDER BY date_time DESC LIMIT 1"
        mycursor.execute(sql)
        dbconn.commit() 
        row = mycursor.fetchone()[0]
        row = (row.replace(' ','T'))+'-05:00'
        return row
    except:
        return '2022-01-01T00:00:00-05:00'

def auth():
    url = 'https://auth.admobilize.com/v2/accounts/-/sessions'
    headers = {'Content-Type':'application/json'}
    data = {'email':'juan.gomez@greencss.com','password': 'Gr33nCS22!'}
    response = requests.post(url,headers=headers,json=data).json()
    return response['accessToken']

def get_job(type,start_time,last_time):
    token = auth()
    url = 'https://datagatewayapi.admobilize.com/v1alpha1/jobs'
    headers = {'Content-Type':'application/json','Authorization':'Bearer ' +str(token)}
    data = {'startTime':start_time,'endTime':last_time,'productId':str(type),'timezone':'America/Bogota'}
    response = requests.post(url,headers=headers,json=data).json()
    return response['jobId'], response['status'], token

def get_data_crowd():
    job_id,status,token = get_job('crowd',get_last_date_crowd(),date_time())
    if status == 'DONE':
        url = 'https://datagatewayapi.admobilize.com/v1alpha1/jobs/'+job_id+'/export?format=csv'
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer ' +token}
        response = requests.get(url,headers=headers).json()
        print()
        res = urlopen(response['urls'][0])
        lines = [l.decode('utf-8') for l in res.readlines()]
        cr = csv.reader(lines)
        dbconn = dbconnection()
        mycursor = dbconn.cursor() 
        cont = 0
        for row in cr:
            if cont > 0:
                sql = "INSERT INTO crowd (device_id, zone_id, event, direction, count, insert_id, device_registry, camera_id, device_name, date_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                mycursor.execute(sql, (str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[5]),str(row[6]),str(row[7]),str(row[8]),str(row[9])))
                dbconn.commit()
            cont = cont + 1
        mycursor.close()
    return 'ok'

def get_data_audience():
    job_id,status,token = get_job('audience',get_last_date_aud(),date_time())
    if status == 'DONE':
        url = 'https://datagatewayapi.admobilize.com/v1alpha1/jobs/'+job_id+'/export?format=csv'
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer ' +token}
        response = requests.get(url,headers=headers).json()
        print()
        res = urlopen(response['urls'][0])
        lines = [l.decode('utf-8') for l in res.readlines()]
        cr = csv.reader(lines)
        dbconn = dbconnection()
        mycursor = dbconn.cursor() 
        cont = 0
        for row in cr:
            if cont > 0:
                sql = "INSERT INTO audience (device_id, emotion, gender, age, is_view, is_impresion, dwell_time, mask, session_time, insert_id, device_registry, camer_id, device_name, date_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                mycursor.execute(sql, (str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[5]),str(row[6]),str(row[7]),str(row[8]),str(row[9]),str(row[10]),str(row[11]),str(row[12]),str(row[13])))
                dbconn.commit()
            cont = cont + 1
        mycursor.close()

# get_data_crowd()
# get_data_audience()
#get_last_date_aud()
