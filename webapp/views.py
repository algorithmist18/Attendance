#Importing libraries
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from webapp.models import Subject, Semester, Schedule_Blob, Profile
from django.db import models
from django.contrib import auth
from webapp.forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from bs4 import BeautifulSoup as bs 
import requests, math, datetime
# Create your views here.
def index(request):

	return render(request, 'homepage.html')

def contact(request):

	return render(request, 'contactpage.html', {'content' : ['Contact us at: afhjfsd']})

def subjects(request):

	return render(request, 'subjects.html')

def semester(request):

	username = request.GET.get('user')
	semester_id = request.GET.get('s_id')
	#Get objects
	user = User.objects.get(username = username)
	semester = Semester.objects.filter(semester_no = semester_id, user = user)[0]
	try:
		subject_list = Subject.objects.all().filter(semester = semester, user = user)
	except Subject.DoesNotExist:
		subject_list = None
	#Create context argument list
	args = {'subjects' : subject_list, 'semester' : semester, 'user' : user}
	if request.method == 'POST': 
		#Request for delete/add
		action = request.POST.get('button')
		if action == 'Delete':
			#Delete semester after alert
			return HttpResponseRedirect('delete?user={}&s_id={}'.format(username, semester_id))
		else:
			#Add subjects
			return HttpResponseRedirect('subjects?user={}&s_id={}'.format(username, semester_id))
	return render(request, 'semester_display.html', args)

def semester_delete(request):

	#Handle deletion of semester

	sem_no = request.GET.get('s_id')
	username = request.GET.get('user')
	user = User.objects.filter(username = username)[0]
	semester = Semester.objects.filter(semester_no = sem_no, user = user)[0]

	args = {'user' : user, 'semester' : semester}

	if request.method == 'POST':

		print('Processing request.')
		action = request.POST.get('button')

		if action == 'Delete':
			semester.delete()
			return HttpResponseRedirect('profile?user={}'.format(username))
		else:
			return HttpResponseRedirect('semester?user={}&s_id={}'.format(username, sem_no))
	return render(request, 'delete_semester.html', {'user' : user, 'semester' : semester})

def visitor_profile(request, visitor, org_user):

	#Visiting a different profile

	current_time = datetime.datetime.now()
	day = str(current_time.strftime("%A"))
	date = datetime.datetime.strptime(current_time.strftime("%Y-%m-%d"), '%Y-%m-%d').date()

	user = User.objects.get(username = visitor)
	semesters = Semester.objects.filter(user = user)	
	print(org_user.username)

	if request.method == 'POST':
		#Search query request
		query = request.POST.get('search')
		print('Query to be searched for = {}'.format(query))
		return HttpResponseRedirect('search?user={}&q={}'.format(org_user.username, query))

	s_list = []
	subject_list = []
	classes_today = []
	current_semester = ''
	l = 0

	for semester in semesters.all():
		s_list.append(semester)
		if semester.start_date < date and semester.end_date > date:
			current_semester = semester

	print('{}\'s current semester = {}'.format(user.username, current_semester))
	timings = ()

	if current_semester != '' and current_semester != None:
		
		subjects = Subject.objects.filter(semester = current_semester, user = user)

		for sub in subjects:
			subject_list.append(sub)

		l = len(s_list) #Number of subjects user has registered

	else:

		#User does not have a semester ready
		pass

	print('User = {}'.format(user.first_name))
	args = {'org_user' : org_user, 'user' : user, 'current_sem' : current_semester, 's_list' : s_list, 'size' : l, 'subjects' : subject_list}
	return args

def profile(request):

	username = request.GET.get('user') #User logged in
	visitor = request.GET.get('q') #User whose profile is being checked out now
	
	user = User.objects.get(username = username)
	semesters = Semester.objects.filter(user = user)	

	if visitor != None and visitor != username:

		print('Visit {}\'s profile.'.format(visitor))
		args = visitor_profile(request, visitor, user)
		return render(request, 'visitor_profile_page.html', args)

	else:

		current_time = datetime.datetime.now()
		day = str(current_time.strftime("%A"))
		date = datetime.datetime.strptime(current_time.strftime("%Y-%m-%d"), '%Y-%m-%d').date()

		if request.method == 'POST':
			#Search query request
			query = request.POST.get('search')
			print('Query to be searched for = {}'.format(query))
			return HttpResponseRedirect('search?user={}&q={}'.format(user.username, query))

		s_list = []
		subject_list = []
		classes_today = []
		current_semester = ''
		l = 0

		for semester in semesters.all():
			if semester.start_date < date and semester.end_date > date:
				current_semester = semester
			else:
				s_list.append(semester)

		timings = ()

		if current_semester != '' and current_semester != None:
			
			subjects = Subject.objects.filter(semester = current_semester, user = user)

			for sub in subjects:
				subject_list.append(sub)
			l = len(s_list) #Number of subjects user has registered


			for classes in Schedule_Blob.objects.all().filter(semester = current_semester, user = user, day = day):
				classes_today.append(classes.subject)

			#Making a routine to display on profile home page
			
			timings_list = []

			blobs = Schedule_Blob.objects.all().filter(user = user, semester = current_semester).order_by('start_time')

			for blob in blobs:
				timings_list.append(blob.start_time)

			if len(blobs) != 0:
				print('Index error not going to happen.')
				period_time = datetime.timedelta(hours = blobs[0].end_time.hour, minutes = blobs[0].end_time.minute) - datetime.timedelta(hours = blobs[0].start_time.hour, minutes = blobs[0].start_time.minute)
				timings = sorted(set(timings_list))
				args = {'user' : user, 'current_sem' : current_semester, 'blobs' : blobs, 'timings' : timings, 'time' : period_time, 's_list' : s_list, 'size' : l, 'subjects' : subject_list, 'classes' : classes_today}
				return render(request, 'profile_page.html', args)
			else:
				#User has no routine ready yet
				args = {'user' : user, 'current_sem' : current_semester, 'message' : 'You do not have a routine ready', 's_list' : s_list, 'size' : l, 'subjects' : subject_list, 'classes' : classes_today}
				return render(request, 'profile_page.html', args)
		else:

			#User does not have a semester ready
			return render(request, 'profile_page.html', {'user' : user, 's_list' : s_list})

	args = {'user' : user, 'current_sem' : current_semester, 'blobs' : blobs, 'timings' : timings, 'time' : period_time, 's_list' : s_list, 'size' : l, 'subjects' : subject_list, 'classes' : classes_today}
	return render(request, 'profile_page.html', args)

def edit_profile(request):

	username = request.GET.get('user')
	user = User.objects.get(username = username)

	args = {'user' : user}

	if request.method == 'POST':

		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		institute = request.POST.get('institute')
		birth_date = request.POST.get('birth_date')

		#Save user details to database
		user.first_name = first_name
		user.last_name = last_name
		user.profile.institute = institute
		user.profile.birth_date = birth_date

		#profile = user.get_profile()
		#profile.institute = institute
		#profile.birth_date = birth_date

		user.profile.save()
		user.save()
		args.update({'message' : 'User profile updated successfully!'})

	return render(request, 'edit_profile.html', args)

def take_subjects(request):

	if request.method == 'POST':
		#Take subject details
		subject_code = request.POST.get('code')
		subject_name = request.POST.get('subject')
		threshold = request.POST.get('threshold')
		username = request.GET.get('user')
		#Save to semester
		user = User.objects.get(username = username)
		semester_no = request.GET.get('s_id')
		semester = Semester.objects.get(user = user, semester_no = semester_no)

		try:
			subject = Subject(semester = semester, user = user, subject = subject_name, code = subject_code, threshold = threshold)
			subject.save()
		except:
			message = 'Subject already exists.'
			return render(request, 'subjects_user.html', {'username' : username, 'semester_no' : semester_no, 'message' : message, 'type' : 'failure'})
		return render(request, 'subjects_user.html', {'username' : username, 'semester_no' : semester_no, 'message' : 'Subject added succesfully.', 'type' : 'success'})
	else:
		username = request.GET.get('user')
		sem_no = request.GET.get('s_id')
		return render(request, 'subjects_user.html', {'username' : username, 'semester_no' : sem_no})

def create_semester(request):

	if request.method == 'POST':

		username = request.GET.get('user')
		start_date = request.POST.get('start_date')
		end_date = request.POST.get('end_date')
		sem_no = request.POST.get('sem')

		if start_date > end_date:

			message = 'Semester cannot end before it starts.'
			return render(request, 'semester_input.html', {'username' : request.GET.get('user'), 'message' : message, 'type' : 'failure'})

		if sem_no == None or sem_no == '' or start_date == None or start_date == '' or end_date == None or end_date == '':

			message = 'All the fields are required.'
			return render(request, 'semester_input.html', {'username' : request.GET.get('user'), 'message' : message, 'type' : 'failure'})

		#Save semester details to database
		user = User.objects.get(username = username)
		try:
			semester = Semester(user = user, start_date = start_date, end_date = end_date, semester_no = sem_no)
			semester.save()
		except:
			message = 'Semester already exists.'
			return render(request, 'semester_input.html', {'username' : request.GET.get('user'), 'message' : message, 'type' : 'failure'})
		#Redirect to subject input page
		return render(request, 'subjects_user.html', {'username' : username, 'semester_no' : sem_no})

	return render(request, 'semester_input.html', {'username' : request.GET.get('user')})

def register(request):

	if request.method == 'POST':

		form = RegistrationForm(request.POST)

		if form.is_valid():


			"""
			email = form.cleaned_data['email']
			password = request.POST.get('password', None)
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')
			username = request.POST.get('username')
			institute = request.POST.get('institute')
			birth_date = request.POST.get('birth_date')
			"""

			#Checking email and username validation

			email = form.cleaned_data['email']
			username = form.cleaned_data['username']

			if User.objects.filter(username = username).exists():

				#Username taken
				return render(request, 'register_page.html', {'form' : form, 'username_error' : 'Username already taken.'})

			if User.objects.filter(email = email).exists():

				#Email ID exists
				print('Email address already taken.')
				return render(request, 'register_page.html', {'form': form, 'email_error' : 'Email already taken.'})

			#Save user to database

			user = form.save()
			user.refresh_from_db()
			user.profile.birth_date = form.cleaned_data.get('birth_date')
			user.profile.institute = form.cleaned_data.get('institute')
			raw_password = form.cleaned_data.get('password2')
			user.set_password(raw_password)
			user.profile.save()
			return render(request, 'homepage.html')
		
		else:
			print(form.errors)
			return render(request, 'register_page.html', {'form' : form})

		args = {'form' : form, 'email' : email, 'username' : username, 'password' : password, 'first_name' : first_name, 'last_name': last_name}
		return render(request, 'subjects_user.html', args)

	else:
		form = RegistrationForm()
		return render(request, 'register_page.html', {'form' : form})

def createUser(username, email, password, first_name, last_name, institute, birth_date):

	user = User.objects.create_user(username = username, password = password, email = email)
	user.last_name = last_name
	user.first_name = first_name

	user.save()

def logout(request):

	return render(request, 'home.html')

def login(request):


	if request.method == 'POST':

		#Attempting to login

		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username = username, password = password)

		if user is not None:

			#Authentication successful

			s = Subject.objects.filter(user = user)
			request.user = user
			args = {'username' : username, 'first_name' : user.first_name}

			if s is None:
				return render(request, 'subjects_user.html', args)
			else:
				return HttpResponseRedirect('profile?user={}'.format(username))

		else:

			#Authentication failure
			return render(request, 'homepage.html')

	return render(request, 'homepage.html')

def summary(request):

	subject_name = request.GET.get('subject')

	if request.method == 'POST':

		sname_list = request.POST.get('sub_name')

	username = request.GET.get('username', '')

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
		
	subject = request.GET.get('subject')
	username = request.GET.get('user')
	sem_id = request.GET.get('s_id')

	u = User.objects.get(username = username)
	s = Subject.objects.filter(user = u, subject = subject)
	semester = Semester.objects.filter(user = u, semester_no = sem_id)[0]

	for ob in s:
		if ob.subject == subject:
			s_name = ob
			break

	if request.method == 'POST':

		action = request.POST.get('action')

		if action == 'Save':
			#TODO: Save everything to database
			ob.user = u
			ob.present = present
			ob.absent = int(total)-int(present)
			ob.safe_bunks = bunks
			ob.notes = notes
			ob.percent = percent[:4]
			ob.total = total 
			ob.save()

		else:
			#TODO: Delete semester after raising warning
			return HttpResponseRedirect('subdelete?user={}&s_id={}&subject={}'.format(username, sem_id, subject))

	args = {'sub' : ob, 'user' : u, 'semester' : semester}

	return render(request, 'subject_summary.html', args)

def delete_subject(request):

	#Function to delete a subject

	subject_name = request.GET.get('subject')
	sem_id = request.GET.get('s_id')
	username = request.GET.get('user')

	user = User.objects.get(username = username)
	subject = Subject.objects.filter(subject = subject_name, user = user)[0]
	semester = Semester.objects.filter(semester_no = sem_id, user = user)[0]

	if request.method == 'POST':
		action = request.POST.get('action')
		if action == 'Delete':
			subject.delete()
			return HttpResponseRedirect('semester?user={}&s_id={}'.format(username, sem_id))
		else:
			return HttpResponseRedirect('showsub?user={}&s_id={}&subject={}'.format(username, sem_id, subject_name))

	args = {'subject' : subject, 'semester' : semester, 'user' : user}
	return render(request, 'delete_subject.html', args)

def fill_routine(request):

	#Method to create the timetable
	sem_id = request.GET.get('s_id')
	username = request.GET.get('user')

	user = User.objects.get(username = username)
	semester = Semester.objects.get(semester_no = sem_id, user = user)	
	subject_list = Subject.objects.all().filter(semester = semester, user = user)

	args = {'user' : user, 'semester' : semester, 'subjects' : subject_list}
	
	if request.method == 'POST':

		start_time = request.POST.get('start_time')
		end_time = request.POST.get('end_time')
		subject_name = request.POST.get('subject')
		day = request.POST.get('day')
		subject = Subject.objects.filter(subject = subject_name, user = user, semester = semester)[0]
		#Create a blob and save it
		blob = Schedule_Blob(day = day, start_time = start_time, end_time = end_time, user = user, semester = semester, subject = subject)
		blob.save()

	return render(request, 'make_routine.html', args)

def display_routine(request):

	#Method to display weekly routine of user
	days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

	username = request.GET.get('user')
	sem_id = request.GET.get('s_id')

	user = User.objects.filter(username = username)[0]
	semester = Semester.objects.filter(user = user, semester_no = sem_id)[0]

	timings_list = []

	blobs = Schedule_Blob.objects.all().filter(user = user, semester = semester).order_by('start_time')

	for blob in blobs:
		timings_list.append(blob.start_time)

	period_time = datetime.timedelta(hours = blobs[0].end_time.hour, minutes = blobs[0].end_time.minute) - datetime.timedelta(hours = blobs[0].start_time.hour, minutes = blobs[0].start_time.minute)
	timings = sorted(set(timings_list))

	args = {'user' : user, 'semester' : semester, 'blobs' : blobs, 'timings' : timings, 'time' : period_time}

	return render(request, 'routine.html', args)


def search_query(request):

	username = request.GET.get('user')
	user = User.objects.all().get(username = username)
	args = {'user' : user}
	query = request.GET.get('q')

	print('Query to be searched = {}'.format(query))
		#Search user
	users = User.objects.all().filter(username = query)
	users_by_name = User.objects.all().filter(first_name = query)

	if users is not None:
		args.update({'users' : users})
		return render(request, 'search_display.html', args)
	else:

		if users_by_name is not None:
			args.update({'users' : users_by_name})
			return render(request, 'search_display.html', args)
		else:
			return render(request, 'search_display.html', args)
		#Search institute
	return render(request, 'search_display.html', args)