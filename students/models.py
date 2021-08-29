from django.db import models
# Create your models here.


class Student(models.Model):
    student_id = models.IntegerField()
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    school_name = models.CharField(max_length=255, null=True)
    subject_name = models.CharField(max_length=255, null=True)
    day_of_week = models.CharField(max_length=15, null=True)
    time_from = models.CharField(max_length=255, null=True)
    time_to = models.CharField(max_length=255, null=True)
    parents_email = models.CharField(max_length=255, null=True)
    zoom_link = models.CharField(max_length=255,null=True)
    meeting_id = models.CharField(max_length=255,null=True)
    zoom_password = models.CharField(max_length=255,null=True)
    

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - {self.student_id}"

