from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
url(r'^home/', views.index, name='index'),
url(r'^contact/', views.contact, name = 'contact'),
url(r'^login', views.login, name = 'login'),
url(r'^logout/', views.logout, name = 'logout'),
url(r'^register', views.register, name = 'register'),
url(r'^subjects', views.take_subjects, name = 'subjects'),
url(r'^summary', views.summary, name = 'summary'),
url(r'^showsub', views.subject_summary, name = 'sub_sum'),
url(r'^profile', views.profile, name = 'profile'),
url(r'^sem_form', views.create_semester, name = 'semester'),
url(r'^semester', views.semester, name = 'show_semester'),
url(r'^delete', views.semester_delete, name = 'delete_sem'),
url(r'^subdelete', views.delete_subject, name = 'delete_sub'),
url(r'^routine', views.fill_routine, name = 'routine'),
url(r'^display', views.display_routine, name = 'display_routine'),
url(r'^edit_profile', views.edit_profile, name = 'edit_profile'),
url(r'^search', views.search_query, name=  'search'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)