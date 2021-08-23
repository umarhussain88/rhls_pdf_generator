CREATE VIEW 
Report.vwStudentAcademicYear
AS 
SELECT 
            st.FirstName
       ,    st.LastName
       ,    st.SchoolLocationId
       ,    em.parents_email
       ,    st.StudentId
       ,    loc.Name as [school_name]
       ,    sub.Name as [subject_name]
       ,    cs.TimeFrom
       ,    cs.TimeTo

FROM School.Students st 
LEFT JOIN School.StudentClasses scl 
     ON   st.StudentId = scl.StudentId
LEFT JOIN school.Classes cl 
     ON   cl.SubjectId = scl.SubjectId
LEFT JOIN Administration.SchoolLocations loc 
     ON   loc.SchoolLocationId = cl.SchoolLocationId
LEFT JOIN Administration.Subjects sub 
     ON   sub.SubjectId = cl.SubjectId
LEFT JOIN School.ClassSchedules cs 
     ON   cs.ScheduleId = scl.ScheduleId

LEFT JOIN (SELECT StudentId
            ,   STRING_AGG(PrimaryEmail + 
                CASE WHEN SecondaryEmail IS NOT NULL 
                THEN 
                ',' + SecondaryEmail
                ELSE ''
                END
            ,  ',') as parents_email 
        FROM School.Students
        GROUP BY StudentId) em
    ON em.StudentId = st.StudentId 

-- need to add filter to get current academic year. 
-- INNER JOIN Administration.SchoolLocationCalendar sc_cal 
--     ON sc_cal.SchoolLocationId = loc.SchoolLocationId
--     -- AND sc_cal.CalendarDate >= '01 Sep 2020'
WHERE scl.StudentId is not null


