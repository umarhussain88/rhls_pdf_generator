from dotenv import load_dotenv
import os 
import pyodbc 

load_dotenv()

## to delete from sqllite table first.
#DELETE FROM students_student; -- deletes table
#DELETE FROM SQLITE_SEQUENCE WHERE name = 'students_student'; -- resets ID column counter

def create_azure_connection():

    
    SERVER       =    os.getenv('server')
    DATABASE     =    os.getenv('database')
    USERNAME     =    os.getenv('username')
    PASSWORD     =    os.getenv('password')
    DRIVER       =    os.getenv('driver')


    azure_con =  pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) 

    return azure_con 

