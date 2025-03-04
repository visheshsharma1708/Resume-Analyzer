from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Candidate, Job
from .forms import ResumeUploadForm
from .serializers import CandidateSerializer
from .utils import extract_text_from_resume, calculate_match_score


def upload_resume(request):
    if request.method == "POST":
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume_instance = form.save()

            # Read resume text safely
            resume_instance.resume.seek(0)  # Reset file pointer
            resume_text = resume_instance.resume.read().decode('utf-8')

            # Calculate match score
            match_score = calculate_match_score(resume_text, resume_instance.job_description)

            # Store the match score in session
            request.session['match_score'] = match_score
            request.session['job_description'] = resume_instance.job_description
            request.session['resume_text'] = resume_text

            return redirect('match_result')  # Redirect to result page
    else:
        form = ResumeUploadForm()

    return render(request, "analyzer/upload.html", {"form": form})


def match_result(request):
    """View to display the match result"""
    match_score = request.session.get('match_score')
    job_description = request.session.get('job_description', "")
    resume_text = request.session.get('resume_text', "")

    if match_score is None:
        messages.error(request, "No result found. Please upload a resume first.")
        return redirect('upload_resume')

    return render(request, "analyzer/result.html", {
        "match_score": match_score,
        "job_description": job_description,
        "resume_text": resume_text
    })


class CandidateUploadView(generics.CreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            candidate = serializer.save()
            resume_text = extract_text_from_resume(candidate.resume)
            job_description = request.data.get("job_description", "")
            match_score = calculate_match_score(resume_text, job_description)

            response_data = CandidateSerializer(candidate).data
            response_data["match_score"] = match_score
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def home(request):
    return render(request, 'analyzer/home.html')


def about(request):
    return render(request, 'analyzer/about.html')


def contact(request):
    return render(request, 'analyzer/contact.html')


def FAQ(request):
    return render(request, 'analyzer/FAQ.html')


def index(request):
    return render(request, 'analyzer/index.html')


def services(request):
    return render(request, 'analyzer/services.html')
