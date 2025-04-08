from django.contrib import admin
from .models import DataChangeLog

@admin.register(DataChangeLog)
class DataChangeLogAdmin(admin.ModelAdmin):
    list_display = ['get_model_name', 'object_id', 'action', 'timestamp', 'user']
    list_filter = ['action', 'content_type', 'user']
    readonly_fields = ['content_type', 'object_id', 'action', 'changes', 'timestamp', 'user']

    @admin.display(description='Model Name')
    def get_model_name(self, obj):
        return obj.content_type.model.capitalize()  # Will show model name like Book, Student etc.
