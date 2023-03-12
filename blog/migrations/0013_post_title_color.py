# Generated by Django 4.1 on 2022-09-02 13:43

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title_color',
            field=colorfield.fields.ColorField(default='#000', image_field=None, max_length=18, samples=[('#FFFFFF', 'white'), ('#f8c0c8', 'pink'), ('#fb9857', 'orange'), ('#d3bbdd', 'purple')]),
        ),
    ]