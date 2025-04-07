from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from .models import Book
from logs.utils import log_data_change
from middleware.current_user import get_current_user
from copy import deepcopy

@receiver(pre_save, sender=Book)
def capture_old_data(sender, instance, **kwargs):
  if instance.pk:
    try:
      old_instance = sender.objects.get(pk=instance.pk)
      instance._old_instance_data = {
        field.name: deepcopy(getattr(old_instance, field.name))
        for field in sender._meta.fields
      }
    except sender.DoesNotExist:
      instance._old_instance_data = None

@receiver(post_save, sender=Book)
def log_create_or_update(sender, instance, created, **kwargs):
  user=get_current_user()
  if created:
    log_data_change(instance, 'CREATE', user)
  else:
    old_data = getattr(instance, '_old_instance_data', None)
    if old_data:
      log_data_change(instance, 'UPDATE', user, old_data)
    else:
      log_data_change(instance, 'UPDATE', user)

@receiver(pre_delete, sender=Book)
def log_delete(sender, instance, **kwargs):
  user=get_current_user()
  log_data_change(instance, 'DELETE', user)