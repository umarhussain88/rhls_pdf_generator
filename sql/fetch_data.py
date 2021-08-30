import os
import sqlite3 as sql

import pandas as pd
import pyodbc
from dotenv import load_dotenv
from sqlalchemy import create_engine
from pathlib import Path

load_dotenv()

server       =    os.getenv('server')
database     =    os.getenv('database')
username     =    os.getenv('username')
password     =    os.getenv('password')
driver       =    os.getenv('driver')


azure_con =  pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) 


df = pd.read_sql('SELECT * FROM Report.vwStudentClasses_2021 where studentid = 775', azure_con)

azure_con.close()

sql_lite_db = list(Path(__file__).parent.parent.glob('*.sqlite3'))[0]

print(sql_lite_db)

engine = create_engine(f"sqlite:///{str(sql_lite_db)}", echo=False)
trg_cols = ["student_first_name","student_last_name","parents_email",
            "StudentId","school_name","subject_name","DAYOFWEEK","TimeFrom","TimeTo","REMARKS"]

df = df[trg_cols]

df = df.rename(columns={
    "student_first_name" : 'first_name',
    "student_last_name" : 'last_name',
    "parents_email" : 'parents_email',
    "StudentId" : 'student_id',
    "school_name" : 'school_name',
    "subject_name" : 'subject_name',
    "DAYOFWEEK" : 'day_of_week',
    "TimeFrom" : 'time_from',
    "TimeTo" : 'time_to',
    })

s = df['REMARKS'].str.replace('\s{2}' ,' ').str.split(' ',expand=True).copy()

df['zoom_link'] = s[0]
df['meeting_id'] = s[[3,4,5]].agg(' '.join,1)
df['zoom_password'] = s[7]

df = df.drop('REMARKS',1)
    
df.to_sql('students_student',index=False,con=engine,if_exists='append')
print('completed writing to sqlite')