
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='cbts-home'),
    path('sign_in', auth_views.LoginView.as_view(template_name='CBTS_APP/sign-in.html'), name='cbts-sign_in'),
    path('register', views.register, name='cbts-register'),
    path('overview', views.overview, name='cbts-overview'),
    path('student', views.student, name='cbts-student'),
    path('test', views.test, name='cbts-test'),
    path('result', views.result, name='cbts-result'),
    path('create-subject', views.create_subject, name='cbts-create-subject'),
    path('view-subject', views.view_subject, name='cbts-view-subject'),
    path('create-topic', views.create_topic, name='cbts-create-topic'),
    path('create-questions', views.create_question, name='cbts-create-question'),
    path('create-choice', views.create_choice, name='cbts-create-choice'),
]
