# Generated by Django 4.1 on 2023-02-13 13:34

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_post_content2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='content2',
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]