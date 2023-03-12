from django.db import models
from django.utils import timezone
from PIL import Image
from makePictureSquare import resize_image 
from colorfield.fields import ColorField
from tinymce.models import HTMLField


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = HTMLField()
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.ImageField(
        default='images/logo.png', upload_to='images/post_headings')
    tags = models.ManyToManyField('PostTag', blank=True)

    COLOR_PALETTE = [
        ("#FFFFFF", "white", ),
        ("#f8c0c8", "pink",),
        ("#fb9857", "orange",),
        ("#d3bbdd", "purple")

    ]
    title_color = ColorField(default='#000', samples=COLOR_PALETTE)


    def __str__(self):
        return self.title

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 400 or img.width > 400:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)
        
        img = Image.open(self.image.path)
        new_img = resize_image(img, 400)
        new_img.save(img.filename)
        


class PostTag(models.Model):
    title = models.CharField(max_length=20, unique=False)

    def __str__(self):
        return self.title


class PostComment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    comment = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    isSubComment = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE,  null=True, blank=True, default=None)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} on {self.post}'


class Podcast(models.Model):
    url = models.CharField(max_length=120)

    def __str__(self):
        return self.url


class Video(models.Model):
    url = models.CharField(max_length=25)

    def __str__(self):
        return self.url


class PDF(models.Model):
    file = models.FileField(upload_to='pdfs')
    picture = models.FileField(
        upload_to='images/pdfHeaders', default="images/logo.png")
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Notification(models.Model):
    email = models.EmailField(max_length=256)

    def __str__(self):
        return self.email
