from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class DataChangeLog(models.Model):
  ACTION_CHOICES = [
    ('CREATE', 'Create'),
    ('UPDATE', 'Update'),
    ('DELETE', 'Delete'),
  ]

  # model_name = models.CharField(max_length=255)
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  object_id = models.PositiveBigIntegerField()
  action = models.CharField(max_length=10, choices=ACTION_CHOICES)
  changes=models.JSONField(null=True, blank=True)
  timestamp = models.DateTimeField(default=now)
  user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

  def __str__(self):
    return f"{self.action} on {self.content_type} ({self.object_id})"

# Create your models here.
