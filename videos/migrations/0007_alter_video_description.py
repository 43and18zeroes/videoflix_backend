# Generated by Django 5.1.7 on 2025-04-25 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_video_video_file_1080p_video_video_file_480p_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='description',
            field=models.TextField(blank=True, max_length=255),
        ),
    ]
