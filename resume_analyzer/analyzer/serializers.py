from rest_framework import serializers
from .models import Candidate
from .utils import extract_text_from_pdf, extract_text_from_docx

class CandidateSerializer(serializers.ModelSerializer):
    extracted_text = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = ['id', 'name', 'resume', 'uploaded_at', 'extracted_text']

    def get_extracted_text(self, obj):
        if not obj.resume:  
            return "No resume uploaded"

        file_path = obj.resume.path  

        if file_path.endswith('.pdf'):
            return extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            return extract_text_from_docx(file_path)
        return "Unsupported file format"
