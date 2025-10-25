from django.db import models

# Create your models here.
# compare/models.py
from django.db import models
from django.contrib.auth.models import User

class TextComparison(models.Model):
    left_text = models.TextField()
    right_text = models.TextField()
    left_diff_html = models.TextField(blank=True)   # HTML for left diff
    right_diff_html = models.TextField(blank=True)  # HTML for right diff
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comparison #{self.id} at {self.created_at}"
