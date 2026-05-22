from django.db import models
from django.conf import settings

class Complaint(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('forwarded', 'Forwarded'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )

    URGENCY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('emergency', 'Emergency'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_anonymous = models.BooleanField(default=False)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100) # Could be extracted by AI
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='low')
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.status}"

class Evidence(models.Model):
    complaint = models.ForeignKey(Complaint, related_name='evidence', on_delete=models.CASCADE)
    file_url = models.URLField(max_length=500) # We will store Cloudinary URLs
    media_type = models.CharField(max_length=50) # image, video, audio, pdf
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evidence for {self.complaint.title}"

class Support(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    complaint = models.ForeignKey(Complaint, related_name='supports', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'complaint')
