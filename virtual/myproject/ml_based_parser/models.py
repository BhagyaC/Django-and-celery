from django.db import models


class ResumeParse(models.Model):
    """
    Model for storing parsed result of candidate's resume
    """
    candidate_id = models.CharField(max_length=255, blank=False)
    document = models.FileField(upload_to='tmp/')  # Tmp folder to store documents for parsing
    document_link = models.CharField(max_length=1024)
    is_parse_successful = models.BooleanField(default=False)
    
    # Fields to measure parsing efficiency
    time_start = models.DateTimeField(null=True)
    time_end = models.DateTimeField(null=True)
    computing_device = models.CharField(max_length=255)  # CPU/GPU version
