# Generated by Django 4.1 on 2022-08-24 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_pdf_picture_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdf',
            name='picture',
            field=models.FileField(default='images/logo.png', upload_to='images/pdfHeaders'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='images/logo.png', upload_to='images/post_headings'),
        ),
    ]