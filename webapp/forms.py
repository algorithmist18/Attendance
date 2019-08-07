from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):

	email = forms.EmailField(required = True)	

class RegistrationForm(UserCreationForm):

	email = forms.EmailField(required = True)
	institute = forms.CharField(max_length = 100)
	birth_date = forms.DateField(help_text = 'Required. Format: YYYY-MM-DD')

	class Meta:

		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'birth_date', 'institute', 'password1', 'password2',)
