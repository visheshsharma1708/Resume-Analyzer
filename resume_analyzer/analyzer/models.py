from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    skills = models.TextField()
    experience = models.TextField()
    education = models.TextField()
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_skills = models.TextField()

    def __str__(self):
        return self.title
