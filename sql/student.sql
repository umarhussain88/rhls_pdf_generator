IF OBJECT_ID('report.VWSTUDENTCLASSES_2021') IS NOT NULL
    DROP VIEW  report.VWSTUDENTCLASSES_2021
GO
CREATE VIEW report.VWSTUDENTCLASSES_2021 AS
SELECT
            s.FirstName                  AS student_first_name
       ,    s.LastName                   AS student_last_name
       ,    s.SchoolLocationId
       ,    em.parents_email
       ,    s.StudentId
       ,    loc.Name                     AS [school_name]
       ,    sub.Name                     AS [subject_name]
       ,    cs.DAYOFWEEK
       ,    cs.TimeFrom
       ,    cs.TimeTo
       ,    REPLACE(cs.REMARKS, '"', '') AS REMARKS
       ,    staff.FIRSTNAME              AS teacher_first_name
       ,    staff.LASTNAME               AS teacher_last_name
       ,    s.GUARDIANFIRSTNAME
       ,    s.GUARDIANLASTNAME
       ,    s.GUARDIANWORKPHONE



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

LEFT JOIN Company.STAFFS staff
      ON cs.STAFFID = staff.STAFFID

WHERE
      1= 1
AND cs.REMARKS IS NOT NULL
