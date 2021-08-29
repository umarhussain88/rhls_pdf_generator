CREATE VIEW REPORT.vwStudentClasses_2021
AS
SELECT
            s.FirstName
       ,    s.LastName
       ,    s.SchoolLocationId
       ,    em.parents_email
       ,    s.StudentId
       ,    loc.Name as [school_name]
       ,    sub.Name as [subject_name]
       ,    cs.DAYOFWEEK
       ,    cs.TimeFrom
       ,    cs.TimeTo
       ,    cs.REMARKS


FROM      school.STUDENTS s

INNER JOIN ADMINISTRATION.SCHOOLTERMS t
    ON    t.SCHOOLTERMID = s.SCHOOLTERMID
    AND   t.SCHOOLTERMID = 1017

LEFT JOIN school.STUDENTCLASSES st_cls
     ON   st_cls.STUDENTID = s.STUDENTID

LEFT JOIN ADMINISTRATION.SUBJECTS sub
     ON   sub.SUBJECTID = st_cls.SUBJECTID
     AND  sub.SCHOOLLOCATIONID = s.SCHOOLLOCATIONID

LEFT JOIN school.CLASSES cls
     ON    cls.SCHOOLLOCATIONID = s.SCHOOLLOCATIONID
     AND   cls.SUBJECTID = sub.SUBJECTID
--      AND   cls.CLASSID = cs.CLASSID
     AND   cls.SCHOOLTERMID = t.SCHOOLTERMID

LEFT JOIN School.ClassSchedules cs
     ON   cs.ScheduleId = st_cls.ScheduleId
     AND  cs.CLASSID = cls.CLASSID

LEFT JOIN ADMINISTRATION.SCHOOLLOCATIONS loc
    ON    loc.SCHOOLLOCATIONID = s.SCHOOLLOCATIONID


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
    ON em.StudentId = s.StudentId

WHERE
      1= 1
AND cs.REMARKS IS NOT NULL
