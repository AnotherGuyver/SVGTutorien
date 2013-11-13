# encoding: utf-8
from django.db import models
from django.contrib.auth.models import User, BaseUserManager, AbstractUser, UserManager
from django.db.models.signals import post_save
from django.conf import settings
import datetime

# User Profile
class TutUser(AbstractUser):
	faculty 		= models.CharField(max_length=40)
	field_of_study 	= models.CharField(max_length=40)

# Tutorium
class Tut(models.Model):
	name 			= models.CharField(max_length=100, unique=True)
	description 	= models.TextField()
	requirements 	= models.TextField()
	notes 			= models.TextField()
	tutor 			= models.ForeignKey(settings.AUTH_USER_MODEL)
	max_users 		= models.DecimalField(max_digits=2, decimal_places=0)

	def __unicode__(self):
		return self.name

# Datum für Tutorium
class TutDate(models.Model):
	date 		= models.DateTimeField(null=True)
	room 		= models.CharField(max_length=5)
	tutorium 	= models.ForeignKey(Tut)
	duration 	= models.DecimalField(max_digits=2, decimal_places=1, null=True)

	def __unicode__(self):
		return str(self.date) + " " + str(self.room)

# Teilnahmen
class Attendance(models.Model):
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL)
	tut 		= models.ForeignKey(Tut)

	def __unicode__(self):
		return str(self.user) +' - '+ str(self.tut)

# Bewerbungen
class TutorSuggestion(models.Model):
	tutor 		= models.ForeignKey(settings.AUTH_USER_MODEL)
	faculty		= models.CharField(max_length=100)
	tutname 	= models.CharField(max_length=100)
	text 		= models.TextField()

	def __unicode__(self):
		return '"'+str(self.tutor) + u'" moechte "' + self.tutname + '" halten.'

#def create_user_callback(sender, instance, **kwargs):
#	tutuser, new = TutUser.objects.get_or_create(user=instance)
#post_save.connect(create_user_callback, User)
