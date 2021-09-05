import os
import sqlite3 as sql

import pandas as pd
import pyodbc
from dotenv import load_dotenv
from sqlalchemy import create_engine
from pathlib import Path
from students.models import Student

load_dotenv()

server       =    os.getenv('server')
database     =    os.getenv('database')
username     =    os.getenv('username')
password     =    os.getenv('password')
driver       =    os.getenv('driver')


## to delete from sqllite table first.
#DELETE FROM students_student; -- deletes table
#DELETE FROM SQLITE_SEQUENCE WHERE name = 'students_student'; -- resets ID column counter

azure_con =  pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) 


df = pd.read_sql("""SELECT * 
                  FROM Report.vwStudentClasses_2021 
                  ORDER BY CAST(CONVERT(varchar(30), TIMEFROM, 102) as datetime) ASC
                  """, azure_con)

azure_con.close()

sql_lite_db = list(Path(__file__).parent.parent.glob('*.sqlite3'))[0]




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

s = df['REMARKS'].str.replace('\s{2}' ,' ',regex=True).str.split(' ',expand=True)

df['zoom_link'] = s[0]
df['meeting_id'] = s[[3,4,5]].agg(' '.join,1)
df['zoom_password'] = s[7]

df = df.drop('REMARKS',axis=1)
    

#delete all records in table before overwriting - this resolves any conflicts by a blanket overwrite with types etc.
Student.objects.all().delete()
print('records deleted')


df.to_sql('students_student',index=False,con=engine,if_exists='append')
print('completed writing to sqlite')