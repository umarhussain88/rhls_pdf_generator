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


df = pd.read_sql('SELECT * FROM Report.vwStudentAcademicYear', azure_con)

azure_con.close()

sql_lite_db = list(Path(__file__).parent.parent.glob('*.sqlite3'))[0]

print(sql_lite_db)

engine = create_engine(f"sqlite:///{str(sql_lite_db)}", echo=True)

df = df[['FirstName','LastName','parents_email','StudentId','school_name','subject_name','TimeFrom','TimeTo']]

df.columns = ['first_name','last_name','parents_email','student_id','school_name','subject_name','time_from','time_to']


df.to_sql('students_student',index=False,con=engine,if_exists='append')