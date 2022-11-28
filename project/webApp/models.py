# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Advisor(models.Model):
    employee_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    campus = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    role = models.CharField(max_length=50)

    class Meta:
        # managed = False
        db_table = 'ADVISOR'


class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    professor_id = models.IntegerField()
    start_date = models.DateField()
    duration = models.IntegerField()
    room_id = models.IntegerField()
    college_id = models.IntegerField()
    credit = models.IntegerField()

    class Meta:
        # managed = False
        db_table = 'COURSE'


class StudentProfile(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)

    class Meta:
        db_table = 'USER'
