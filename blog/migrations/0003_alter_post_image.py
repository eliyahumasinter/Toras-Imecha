# Generated by Django 4.0.1 on 2022-07-26 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_postcomment_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='media/images/logo.png', upload_to='images/post_headings'),
        ),
    ]