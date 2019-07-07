from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Semester(models.Model):

	user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
	start_date = models.DateField()
	end_data = models.DateField()

class Subject(models.Model):

	semester = models.ForeignKey(Semester, on_delete = models.SET_NULL, null = True)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)

	present = models.IntegerField(default = 0)
	absent = models.IntegerField(default = 0)
	cancel = models.IntegerField(default = 0)

	threshold = models.FloatField(default = 50.00)
	safe_bunks = models.IntegerField(default = 0)

	total = models.IntegerField(default = 0)
	percent = models.FloatField(default = 0.00)
	notes = models.CharField(max_length = 140, default = '')
	subject = models.CharField(max_length = 50)

class Register(models.Model):

	user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
	date = models.DateTimeField()
	subject = models.ForeignKey(Subject, on_delete = models.SET_NULL, null = True)