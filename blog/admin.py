from django.contrib import admin
from .models import Post, PostTag, PostComment, Podcast, Video, PDF, Notification

admin.site.register(Post)
admin.site.register(PostTag)
admin.site.register(PostComment)
admin.site.register(Podcast)
admin.site.register(Video)
admin.site.register(PDF)
admin.site.register(Notification)
