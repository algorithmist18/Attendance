from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Semester(models.Model):

	user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
	start_date = models.DateField()
	end_date = models.DateField()
	semester_no = models.IntegerField(default = 0)

	class Meta:

		unique_together = ('user', 'semester_no', 'start_date', 'end_date',)

class Subject(models.Model):

	semester = models.ForeignKey(Semester, on_delete = models.SET_NULL, null = True)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)

	code = models.CharField(max_length = 10)
	present = models.IntegerField(default = 0)
	absent = models.IntegerField(default = 0)
	cancel = models.IntegerField(default = 0)

	threshold = models.FloatField(default = 50.00)
	safe_bunks = models.IntegerField(default = 0)

	total = models.IntegerField(default = 0)
	percent = models.FloatField(default = 0.00)
	notes = models.CharField(max_length = 140, default = '')
	subject = models.CharField(max_length = 50)

	class Meta:

		unique_together = ('user', 'code', 'semester',)

class Schedule_Blob(models.Model):

	day = models.CharField(max_length = 10)
	start_time = models.TimeField()
	end_time = models.TimeField()
	subject = models.ForeignKey(Subject, on_delete = models.SET_NULL, null = True)
	semester = models.ForeignKey(Semester, on_delete = models.SET_NULL, null = True)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)

	class Meta:

		unique_together = ('day', 'start_time', 'end_time', 'user', 'semester',)

class Profile(models.Model):

	user = models.OneToOneField(User, on_delete = models.CASCADE)
	institute = models.CharField(max_length = 100, blank = True)
	location = models.CharField(max_length = 25, default='Kolkata')
	birth_date = models.DateField(null=True, blank=True)
	is_online = models.BooleanField(default = False)

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()	
	