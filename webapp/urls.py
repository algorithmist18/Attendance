from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
url(r'^home/', views.index, name='index'),
url(r'^contact/', views.contact, name = 'contact'),
url(r'^subjects/', views.subjects, name = 'subjects'),
url(r'^login', views.login, name = 'login'),
url(r'^logout/', views.logout, name = 'logout'),
url(r'^register', views.register, name = 'register'),
path('views', views.takeSubjects, name = 'takeSubjects'),
url(r'^summary', views.summary, name = 'summary'),
url(r'^subjectsummary', views.subject_summary, name = 'sub_sum')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)