
#Importing libraries
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from webapp.models import Subject
from django.db import models
from django.contrib import auth
from webapp.forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from bs4 import BeautifulSoup as bs 
import requests
# Create your views here.

def index(request):

	print('Called.')
	return render(request, 'homepage.html')

def contact(request):

	return render(request, 'contactpage.html', {'content' : ['Contact us at: afhjfsd']})

def subjects(request):

	return render(request, 'subjects.html')

def register(request):

	email = ' '

	if request.method == 'POST':

		form = LoginForm(request.POST)

		if form.is_valid():

			print('Form is valid.')

			email = form.cleaned_data['email']
			password = request.POST.get('password', None)
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')
			username = request.POST.get('username')

			createUser(username, email, password, first_name, last_name)

			print(email)

		else:

			print(form.errors)

		args = {'form' : form, 'email' : email, 'username' : username, 'password' : password, 'first_name' : first_name, 'last_name': last_name}

		return render(request, 'subjects_user.html', args)

	else:
		print('GET method called.')
		form = LoginForm()
		if form.is_valid():
			email = form.cleaned_data['email']
			print(email)
		return render(request, 'register_page.html', {'form' : form, 'email' : email})

def createUser(username, email, password, first_name, last_name):

	user = User.objects.create_user(username = username, password = password, email = email)
	user.last_name = last_name
	user.first_name = first_name
	user.save()

def takeSubjects(request):

	print('Method takeSubjects() entered.')	

	subject = request.POST.get('subject')
	username = request.GET.get('username', '')
	threshold = request.POST.get('threshold', '')
	var = "subject"

	f = 0

	print('{} has subject {}'.format(username, subject))

	try:

		user = User.objects.get(username = username)
		first_name = user.first_name
		if threshold is not '':
			print('Adding threshold {} to database.'.format(threshold))
			user.threshold = threshold
		else:
			print('Enter proper threshold.')

	except User.DoesNotExist:

		print('User does not exist in database.')

	print('Subject value right now = {}'.format(subject))

	if subject is not None and subject != var and subject != '':

		print('Subject database created for {} adding subject {}'.format(username, subject))
		print('Control here..')

		s_user = Subject(subject = subject, user = user)
		s_list = Subject.objects.filter(subject = subject)
		f = 0

		for s in s_list:

			if s.user == user:
				f = 1

		if(f == 1):
			print('Subject and user already exist.')
		else:
			s_user.save()
			
	args = {'username' : username, 'first_name' : first_name}

	return render(request, 'subjects_user.html', args)

def logout(request):

	return render(request, 'home.html')

def login(request):

	username = ' '
	password = ' '
	print('Called.')

	if request.method == 'POST':

		print('Attempting to login..')

		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username = username, password = password)

		if user is not None:

			s = Subject.objects.filter(user = user)
			args1 = {'username' : username, 'first_name' : user.first_name}

			if s is None:
				return render(request, 'subjects_user.html', args1)
			else:
				s_list = []

				for e in s.all():
					s_list.append(e)

				l = len(s_list) #Number of subjects user has registered

				args2 = {'user' : user, 's_list' : s_list, 'size' : l}

				#Redirect to profile page

				return render(request, 'profile_page.html', args2)
				"""
				if l <= 0:
					return render(request, 'subjects_user.html', args1)
				else:
					#Redirect to 
					return render(request, 'summary_user.html', args2);
				"""
		else:
			message = 'Invalid Username'
			print('Password do not match.')
			return render(request, 'homepage.html')

	return render(request, 'homepage.html')

def summary(request):

	subject_name = request.GET.get('subject')

	if request.method == 'POST':

		print('Post request sent.')
		sname_list = request.POST.get('sub_name')
		print(sname_list)

	username = request.GET.get('username', '')
	print('Method summary() entered with username {}'.format(username))

	try:
		user = User.objects.get(username = username)
		try:

			q = Subject.objects.filter(user = user)
			s_list = []

			for e in q.all():
				s_list.append(e)

			print(Subject.objects.filter(user = user).values_list('subject'))

		except Subject.DoesNotExist:

			s_user = Subjects(subject = subject, user = user)

	except User.DoesNotExist:

		print('User does not exist in database.')

	l = len(s_list)

	args = {'user' : user, 's_list' : s_list, 'length' : l}

	return render(request, 'summary_user.html', args)

def subject_summary(request):

	if request.method == 'POST':

		data = request.POST.copy()
		present = request.POST.get('s_present')
		total = data.get('s_total')
		bunks = data.get('s_bunks')
		notes = data.get('s_notes')
		percent = data.get('s_percent')

		print(present)
		print(bunks)
		print(notes)
		print(total)

	print('subject_summary() entered.')

	subject = request.GET.get('subject', '')
	username = request.GET.get('username', '')

	u = User.objects.get(username = username)
	s = Subject.objects.filter(user = u, subject = subject)

	for ob in s:
		if ob.subject == subject:
			s_name = ob
			break

	if request.method == 'POST':
		#TODO: Save everything to database
		ob.user = u
		ob.present = present
		ob.absent = int(total)-int(present)
		ob.safe_bunks = bunks
		ob.notes = notes
		ob.percent = percent[:4]
		ob.total = total 
		ob.save()

	args = {'sub' : ob, 'username' : username}
	return render(request, 'subject_summary.html', args)