from django.contrib import admin

# Register your models here.
from .models import DataChangeLog

@admin.register(DataChangeLog)
class DataChangeLogAdmin(admin.ModelAdmin):
  list_display = ['model_name', 'object_id', 'action', 'timestamp', 'user']
  list_filter = ['action', 'model_name', 'user']
  readonly_fields = ['model_name', 'object_id', 'action', 'changes', 'timestamp', 'user']
