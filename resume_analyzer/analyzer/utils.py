from django.shortcuts import render
from .forms import ResumeUploadForm
from .models import Candidate
import PyPDF2
import docx

# Function to extract text from resume
def extract_text_from_resume(resume_file):
    text = ""
    if resume_file.name.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(resume_file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    elif resume_file.name.endswith('.docx'):
        doc = docx.Document(resume_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

# Function to calculate match score
def calculate_match_score(resume_text, job_description):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())
    common_words = resume_words.intersection(job_words)
    score = (len(common_words) / len(job_words)) * 100 if job_words else 0
    return round(score, 2)

# View for uploading resumes
def upload_resume(request):
    if request.method == "POST":
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()  # This automatically saves to the database
            resume_text = extract_text_from_resume(candidate.resume)
            job_description = request.POST.get("job_description", "")
            match_score = calculate_match_score(resume_text, job_description)
            return render(request, 'result.html', {'candidate': candidate, 'match_score': match_score})
    else:
        form = ResumeUploadForm()
    return render(request, 'upload.html', {'form': form})
