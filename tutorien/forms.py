from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import Textarea, Select
from tutorien.models import Tut, TutDate, TutUser

'''
class RegistrationForm(ModelForm):
	username	= forms.CharField(label = (u'User Name'))
	email 		= forms.EmailField(label = (u'E-Mail'))
	password 	= forms.CharField(label = (u'Password'), widget = forms.PasswordInput(render_value = False) ) #reder_value=false versteckt die Eingabe
	passwordV	= forms.CharField(label = (u'Verify Password'), widget = forms.PasswordInput(render_value = False) )

	class Meta:
		model = TutUser
		exclude = ('user',)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:										# versuche folgendes:
			User.objects.get(username=username)		# hol alle User mit dem Usernamen=username
		except User.DoesNotExist:					# wenn du nichts findest, wirf Exception "DoesNotExist"
			return username 						# und gib den User zurueck
		raise forms.ValidationError("That username is already taken, please select another.") # ansonsten raise einen forms.ValidationError

	def clean(self):
		password = self.cleaned_data['password']
		passwordV = self.cleaned_data['passwordV']

		if password != passwordV:
			raise form.ValidationError("Passwords did not match. Please try again!")
		return self.cleaned_data
'''
class LoginForm(forms.Form):
	username 	= forms.CharField(label=(u'Username'))
	password 	= forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))

class CreateTutForm(forms.ModelForm):
	name = 			forms.CharField(label = (u'Name des Tutoriums'), required = True)
	description = 	forms.CharField(label = (u'Beschreibung'), widget=Textarea, required = True)
	requirements =	forms.CharField(label = (u'Voraussetzungen'), widget=Textarea, required = False)
	notes =			forms.CharField(label = (u'Bemerkungen'), widget=Textarea, required = False)
	tutor =			forms.ModelChoiceField(TutUser.objects.filter(groups__name='Tutor'), label = (u'Tutor'), required = True)
	max_users =		forms.CharField(label = (u'Teilnehmer'), required = True, widget=Select( choices=((5, '5 Teilnehmer'),(10, '10 Teilnehmer'),(15, '15 Teilnehmer'),(20,'20 Teilnehmer'),(25,'25 Teilnehmer'),(30,'30 Teilnehmer'),(9999,'keine Begrenzung')) ) )

	class Meta:
		model = Tut

class TutorSuggestionForm(forms.Form):
	tutname 	= forms.CharField(label = (u'Name des Tutoriums'), required = True)
	text 		= forms.CharField(label = (u'Bewerbungstext'), required = True, widget=Textarea)



