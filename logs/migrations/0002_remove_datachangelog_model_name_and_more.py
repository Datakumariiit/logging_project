# Generated by Django 4.2.8 on 2025-04-08 11:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('logs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datachangelog',
            name='model_name',
        ),
        migrations.AddField(
            model_name='datachangelog',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
            preserve_default=False,
        ),
    ]
