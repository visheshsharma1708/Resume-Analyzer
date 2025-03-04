from django.contrib import admin
from analyzer.models import Candidate
from analyzer.models import Job
from django.contrib import admin


admin.site.site_header = "Resume Analyzer Admin"
admin.site.site_title = "Resume Analyzer"
admin.site.index_title = "Welcome to Resume Analyzer Dashboard"

admin.site.register(Candidate)
admin.site.register(Job)
# Register your models here.
