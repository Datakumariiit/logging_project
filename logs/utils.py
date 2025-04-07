from .models import DataChangeLog

def log_data_change(instance, action, user=None, old_data=None):
    def serialize_instance(instance):
        return {
            field.name: str(getattr(instance, field.name))  # 👈 Convert all to strings
            for field in instance._meta.fields
        }

    changes = None
    if action == 'UPDATE' and old_data:
        after_data = serialize_instance(instance)
        # Convert old_data values to string too
        old_data_serialized = {k: str(v) for k, v in old_data.items()}
        changes = {'before': old_data_serialized, 'after': after_data}
    else:
        changes = {
            'data': serialize_instance(instance)
        }

    DataChangeLog.objects.create(
        model_name=instance.__class__.__name__,
        object_id=instance.pk,
        action=action,
        changes=changes,
        user=user
    )
