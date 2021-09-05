import os
import sqlite3 as sql

import pandas as pd
import pyodbc
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

server       =    os.getenv('server')
database     =    os.getenv('database')
username     =    os.getenv('username')
password     =    os.getenv('password')
driver       =    os.getenv('driver')


azure_con =  pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) 


df = pd.read_sql('SELECT * FROM Report.vwStudentClasses_2021', azure_con)

cols = {'student_first_name': 'student_first_name',
 'student_last_name': 'student_last_name',
 'SchoolLocationId': 'SchoolLocationId',
 'parents_email': "Parent's Emails",
 'StudentId': 'Student ID ',
 'school_name': 'School Location',
 'subject_name': 'Subject Name',
 'DAYOFWEEK': 'Day of Week',
 'TimeFrom': 'Time From',
 'TimeTo': 'Time To',
 'REMARKS': 'REMARKS',
 'teacher_first_name': 'teacher_first_name',
 'teacher_last_name': 'teacher_last_name',
 'GUARDIANFIRSTNAME': 'GUARDIANFIRSTNAME',
 'GUARDIANLASTNAME': 'GUARDIANLASTNAME',
 'GUARDIANWORKPHONE': 'Guardian Phone Number'}


s = df['REMARKS'].str.replace('\s{2}' ,' ',regex=True).str.split(' ',expand=True)

df['Zoom Link'] = s[0]
df['Zoom Meeting ID'] = s[[3,4,5]].agg(' '.join,1)
df['Zoom Password'] = s[7]

df = df.drop('REMARKS',axis=1)

df = df.rename(columns=cols)

# dirty function to agg string names and drop the cols. 
def agg_str_cols(df, fn, ln, col_name, agg_sep=' '):
    df[col_name] = df[fn] + agg_sep + df[ln]
    df = df.drop([fn, ln],axis=1)

df = df.fillna('') 

agg_str_cols(df,'student_first_name','student_last_name','Student Name')
agg_str_cols(df,'teacher_first_name','teacher_last_name', 'Teacher Name')
agg_str_cols(df,'GUARDIANFIRSTNAME','GUARDIANLASTNAME', 'Guardian Name')

col_order = ['School Location', 'Day of Week', 'Grade',
            'Subject Name', 'Time From', 'Time To','Teacher Name',
            'Student Name', 'Guardian Name', 'Guardian Phone Number',
            'Primary Email', 'Secondary Email',
            'Zoom Link','Zoom Meeting ID','Zoom Password'
            ]

df = df[col_order]

p = Path(__file__).parent.parent.joinpath('export/class_schedule_by_school.xlsx')

xl = pd.ExcelWriter(p)

df.to_excel(xl,sheet_name='master',index=False)

for school,d in df.groupby('School Location'):
    d.to_excel(xl,sheet_name=school[:31],index=False)


xl.save() 
print('----------- file exported ------------------------')




