from base.base_model import BaseModel
from django.db import models
from django.utils import timezone
from account.models import User

class ContactSubmission(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='contact')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(default=timezone.now)
    is_responded = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Contact from {self.name} - {self.subject}"