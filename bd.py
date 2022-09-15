import traceback
import MySQLdb

def dbconnection():
    try:
        return MySQLdb.connect(database='admobilize', user='adin_transelca', password='Adintello20201', host='adintelo-db.cpva49myawem.us-east-2.rds.amazonaws.com')
    except:
        print(traceback.format_exc()) 
