# Generated by Django 4.1 on 2022-08-24 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_pdf_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='images/logo.png', upload_to='public_html/media/images/post_headings'),
        ),
    ]
