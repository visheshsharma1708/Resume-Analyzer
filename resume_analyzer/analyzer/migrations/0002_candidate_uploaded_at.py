# Generated by Django 5.1.6 on 2025-02-18 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default='2025-02-18 10:30:00'),
            preserve_default=False,
        ),
    ]
