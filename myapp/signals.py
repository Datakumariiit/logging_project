from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.apps import apps
from logs.utils import log_data_change
from middleware.current_user import get_current_user

# Define models to track by app_label.model_name
TRACKED_MODELS = [
    'myapp.Book',
    'myapp.Student',
    # 'myapp.Publisher',
    # add more as needed
]

def get_model_class(path):
    app_label, model_name = path.split('.')
    return apps.get_model(app_label, model_name)

# Connect signals for each model
for model_path in TRACKED_MODELS:
    model = get_model_class(model_path)

    def capture_old_data(sender, instance, **kwargs):
        if instance.pk:
            try:
                old_instance = sender.objects.get(pk=instance.pk)
                instance._old_instance_data = {
                    field.name: getattr(old_instance, field.name)
                    for field in sender._meta.fields
                }
            except sender.DoesNotExist:
                instance._old_instance_data = None

    def log_create_or_update(sender, instance, created, **kwargs):
        user = get_current_user()
        if created:
            log_data_change(instance, 'CREATE', user)
        else:
            old_data = getattr(instance, '_old_instance_data', None)
            if old_data:
                log_data_change(instance, 'UPDATE', user, old_data)

    def log_delete(sender, instance, **kwargs):
        user = get_current_user()
        log_data_change(instance, 'DELETE', user)

    # Connect signals
    pre_save.connect(capture_old_data, sender=model)
    post_save.connect(log_create_or_update, sender=model)
    pre_delete.connect(log_delete, sender=model)
