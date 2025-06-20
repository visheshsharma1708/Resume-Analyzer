from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from .models import Candidate, Job
from .forms import ResumeUploadForm
from .serializers import CandidateSerializer, ResumeSerializer
from .utils import extract_text_from_resume, calculate_match_score, extract_text, get_match_score

def upload_resume(request):
    if request.method == "POST":
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume_instance = form.save()
            resume_text = extract_text_from_resume(resume_instance.resume)

            if not resume_text.strip():
                messages.error(request, "Could not extract text from the uploaded resume. Please try a different file.")
                return redirect('upload_resume')

            job_description = resume_instance.job_description
            if not job_description.strip():
                messages.error(request, "Job description is missing. Please enter a valid job description.")
                return redirect('upload_resume')

            match_score, missing_keywords = calculate_match_score(resume_text, job_description)

            request.session['match_score'] = match_score
            request.session['job_description'] = job_description
            request.session['resume_text'] = resume_text
            request.session['missing_keywords'] = missing_keywords
            request.session['candidate_name'] = resume_instance.name

            return redirect('match_result')
    else:
        form = ResumeUploadForm()

    return render(request, "analyzer/upload.html", {"form": form})

def match_result(request):
    match_score = request.session.get('match_score')
    job_description = request.session.get('job_description', "")
    resume_text = request.session.get('resume_text', "")
    missing_keywords = request.session.get('missing_keywords', [])
    candidate_name = request.session.get('candidate_name', "Unknown")

    if match_score is None:
        messages.error(request, "No result found. Please upload a resume first.")
        return redirect('upload_resume')

    return render(request, "analyzer/result.html", {
        "match_score": match_score,
        "job_description": job_description,
        "resume_text": resume_text,
        "missing_keywords": missing_keywords,
        "candidate_name": candidate_name
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

            if not resume_text.strip():
                return Response({"error": "Resume text extraction failed."}, status=status.HTTP_400_BAD_REQUEST)

            job_description = request.data.get("job_description", "")
            if not job_description.strip():
                return Response({"error": "Job description is required."}, status=status.HTTP_400_BAD_REQUEST)

            match_score, missing_keywords = calculate_match_score(resume_text, job_description)
            response_data = CandidateSerializer(candidate).data
            response_data["match_score"] = match_score
            response_data["missing_keywords"] = missing_keywords
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResumeAnalyzerView(APIView):
    def post(self, request):
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES['file']
            job_desc = serializer.validated_data['job_description']
            resume_text = extract_text(file)

            if not resume_text.strip():
                return Response({"error": "Failed to extract text from resume."}, status=status.HTTP_400_BAD_REQUEST)

            score, missing = get_match_score(resume_text, job_desc)
            return Response({
                'match_percentage': score,
                'missing_keywords': missing
            })
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
