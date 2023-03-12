from django.urls import path, re_path
from . import views
from .views import PostDetailView, Blog
import django

def custom_page_not_found(request):
    return django.views.defaults.page_not_found(request, None)

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='blog-post'),
    path('posts/', Blog.as_view(), name="blog-posts"),
    path('tagdetails/<_tag>', views.tagDetails, name='blog-tagdetails'),
    path('audio/', views.audio, name='blog-audio'),
    path('video/', views.video, name='blog-video'),
    path('audio/<str:query>/', views.audioSearchResults,
         name='blog-audioSearchResults'),
    path('pdfs/', views.downloads, name='blog-downloads'),
    path('notifications/', views.notifications, name='blog-notifications'),
    path("404/", custom_page_not_found),
    
]
