from django.db import models
# Create your models here.


class Student(models.Model):
    student_id = models.IntegerField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    school_name = models.CharField(max_length=255)
    subject_name = models.CharField(max_length=255)
    time_from = models.CharField(max_length=255)
    time_to = models.CharField(max_length=255)
    parents_email = models.CharField(max_length=255)
    

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - {self.student_id}"

