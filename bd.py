import traceback
import pyodbc

def dbconnection():
    try:
        return pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
            "Server=ia2.database.windows.net;"
            "Database=IA2;"
            "UID=Greenia2;"
            "PWD=Green2022;")
    except:
        print(traceback.format_exc())
