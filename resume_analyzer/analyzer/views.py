from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Candidate, Job
from .utils import extract_text_from_pdf,extract_text_from_docx
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CandidateSerializer

class CandidateUploadView(generics.CreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            candidate = serializer.save()
            return Response(CandidateSerializer(candidate).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
