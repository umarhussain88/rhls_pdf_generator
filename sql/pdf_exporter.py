import os
import sqlite3 as sql
from pathlib import Path

import pandas as pd
import pdfkit
import pyodbc
from dotenv import load_dotenv

load_dotenv()

server       =    os.getenv('server')
database     =    os.getenv('database')
username     =    os.getenv('username')
password     =    os.getenv('password')
driver       =    os.getenv('driver')


azure_con =  pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) 


df = pd.read_sql("""SELECT StudentId
                                    , parents_email 
                                    , FirstName + ' ' + LastName as student_name
                                    , school_name
                       FROM Report.vwStudentClasses_2021""", azure_con)



start_url = 'http://127.0.0.1:8000/search/?student_id'


options = {
    'page-size': 'A4',
    'margin-top': '0.0in',
    'margin-right': '0.0in',
    'margin-bottom': '0.0in',
    'margin-left': '0.0in' }

for (student,name,email,school),value in df.groupby(['StudentId','student_name','parents_email','school_name']):
    new_url = f"{start_url}={student}"

    trg_dir = Path(__file__).parent.parent.joinpath('export')
    if not trg_dir.is_dir():
        Path.mkdir(trg_dir)
    
    trg_dir_email = trg_dir.joinpath(f'{email}')
    if not trg_dir_email.is_dir():
        Path.mkdir(trg_dir_email)

    trg_path = trg_dir_email.joinpath(f'{name} - {student} - {school}.pdf')

    pdfkit.from_url(new_url, str(trg_path),options=options)
