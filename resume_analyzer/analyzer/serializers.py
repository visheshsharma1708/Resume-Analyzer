from rest_framework import serializers
from .models import Candidate
from .utils import extract_text_from_resume  # Import the correct function

class CandidateSerializer(serializers.ModelSerializer):
    extracted_text = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = ['id', 'name', 'resume', 'uploaded_at', 'extracted_text']

    def get_extracted_text(self, obj):
        if not obj.resume:  
            return "No resume uploaded"

        return extract_text_from_resume(obj.resume)  # Use the correct function
