from django.urls import path
from .import views
from .views import upload_resume, CandidateUploadView
from .views import index, about, contact, FAQ, home, services,match_result
urlpatterns = [
     path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('FAQ/', views.FAQ, name='FAQ'),
    path('home/', views.home, name='home'),
    path('services/', views.services, name='services'),
    path("result/",views.match_result, name="match_result"),
    path('upload/', views.upload_resume, name='upload_resume'), 
    path('api/upload/', CandidateUploadView.as_view(), name='api_upload_resume'), 
]
