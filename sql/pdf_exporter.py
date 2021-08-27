import os
import sqlite3 as sql

import pandas as pd
import pyodbc
from dotenv import load_dotenv
import pdfkit

load_dotenv()

server       =    os.getenv('server')
database     =    os.getenv('database')
username     =    os.getenv('username')
password     =    os.getenv('password')
driver       =    os.getenv('driver')


azure_con =  pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) 


students = pd.read_sql('SELECT TOP 5 StudentId FROM Report.vwStudentAcademicYear', azure_con)['StudentId'].unique().tolist()


start_url = 'http://127.0.0.1:8000/search/?student_id'

for student in students:
    new_url = f"{start_url}={student}"
    pdfkit.from_url(new_url, f'{student}.pdf')
