from django.urls import path
from .views import CandidateUploadView

urlpatterns = [
    path('upload/', CandidateUploadView.as_view(), name='upload_candidate_resume'),
]
