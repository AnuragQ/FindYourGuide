# Generated by Django 5.0.2 on 2024-03-23 23:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_loginsession'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('feedback', models.TextField()),
                ('ip_address', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=255)),
                ('browser_info', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='feedbacks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
