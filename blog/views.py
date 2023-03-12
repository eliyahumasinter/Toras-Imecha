from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Post, PostTag, PostComment, Podcast, Video, PDF, Notification
import os
from torasImecha.settings import ADMIN_EMAIL, GOOGLE_RECAPTCHA_SECRET_KEY
from sendmail import SendEmail
import urllib
import urllib.request
import json
from django.http import HttpResponseNotFound
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials




def error_404_handler(request, exception):
    return HttpResponseNotFound("hello")    


def notifications(request):
    
    if request.method == 'POST':
        check = request.POST['check']
        if check == "":
            email = request.POST['email']
            notification = Notification(email=email)
            notification.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Thank you for subscribing!')
        else:
            messages.add_message(request, messages.ERROR,
                                 "You're a bot")
    return redirect('blog-home')

        
        


def home(request):
    if request.method == 'POST':
        # recaptcha_response = request.POST.get('g-recaptcha-response')
        # url = 'https://www.google.com/recaptcha/api/siteverify'
        # values = {
        #     'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
        #     'response': recaptcha_response
        #     }
        # data = urllib.parse.urlencode(values).encode()
        # req =  urllib.request.Request(url, data=data)
        # response = urllib.request.urlopen(req)
        # result = json.loads(response.read().decode())
        check = request.POST['check']
        allowed = True
        notAllowedList = ["<a>", "http", ".com", ".org", ".net"]
        if check == "":
            name = request.POST['name']
            email = request.POST["email"]
            subject = request.POST["subject"]
            message = request.POST["message"]
            for i in notAllowedList:
                if i in message or i in subject or i in name:
                    allowed = False
                    break
                
            if "noreply" in email:
                allowed = False
            if not allowed:
                messages.add_message(request, messages.ERROR,
                                     'You may not send links')
                return redirect('blog-home')
            completeMessage = f"From: {name}\nEmail: {email}\nMessage: {message}"
            try:
                SendEmail("You received mail from your website",
                      completeMessage, ADMIN_EMAIL).start()
                messages.add_message(request, messages.SUCCESS,
                                     'Your message has been sent!')
            except:
                messages.add_message(request, messages.ERROR,
                                     'Something went wrong on our end ):')
            return redirect('blog-home')
        else:
            messages.add_message(request, messages.ERROR,
                                     'Invalid Captcha')

    else:
                
        os.environ['SPOTIPY_CLIENT_ID'] = '8e86bb656489407cb200aa8cc4118618'
        os.environ['SPOTIPY_CLIENT_SECRET'] = 'a93435c440204c3b9b4a5504b046495c'
        torasImechaID='4VVexLh69qXMSBbe29DyQF'
        print(torasImechaID)
        error = None
        try:
            spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
            results = spotify.show_episodes(torasImechaID, limit=6, market='US')
            print(results)  
            results=results['items']
        except Exception as e:
            print(e)
            error = e
        urls = []
        for podcast in results:
            url = podcast['external_urls']['spotify']
            urls.append(url.lstrip('https://open.spotify.com/episode/'))
        context = {
            'posts': Post.objects.order_by('-date_posted')[:8],
            'tags': PostTag.objects.all(),
            # get most recent podcasts for home page
            'podcasts': urls, #Podcast.objects.order_by('-pk')[:6]
            'error': error
        }
        return render(request, "blog/home.html", context=context)


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        pk = self.kwargs['pk']
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        data = list(Post.objects.filter(
            pk=pk).first().postcomment_set.filter(approved=True))
        comments = []
        for comment in data:
            if comment.parent == None:
                comments.append(comment)
            else:
                place = comments.index(comment.parent)
                comments.insert(place + 1, comment)

        context['comments'] = comments
        context['posts'] = Post.objects.order_by("-date_posted")[:10]
        context['tags'] = PostTag.objects.all()
        return context

    def post(self, request, pk):
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        isSubComment = request.POST['isComment']
        IDToRespondTo = request.POST['IDToRespondTo']
        post = Post.objects.filter(pk=pk).first()
        parent = None
        if isSubComment == "True":
            print(IDToRespondTo)
            parent = PostComment.objects.filter(pk=int(IDToRespondTo)).first()
            print(parent)
      #  try:
        if name and email and message:
            comment = PostComment(
                name=name, email=email, comment=message, post=post, isSubComment=isSubComment, parent=parent)
            comment.save()
            url = f"https://torasimecha.com/admin/blog/postcomment/{comment.pk}/change/#id_approved"
            messages.add_message(request, messages.SUCCESS,
                                 'Your comment has been sent for approval!')

            completeMessage = f"From: {name}\nEmail: {email}\nOn post:{post} \nMessage: {message}\nYou can approve it here: {url}"

            try:
                SendEmail("Comment has been submitted for review",
                          completeMessage, ADMIN_EMAIL).start()
            except:
                messages.add_message(request, messages.ERROR,
                                     'Something went wrong')
            return redirect('blog-post', pk=pk)
        else:
            messages.add_message(request, messages.ERROR,
                                 'The form information is incorrect ):')
    # except:
        messages.add_message(request, messages.ERROR,
                             'Something went wrong ):')
        return redirect('blog-post', pk=pk)


def about(request):
    return render(request, "blog/about.html")


def audio(request):
    results = []
    search = False
    if request.method == "POST":
        query = request.POST.get("search_query").strip()
        return redirect("blog-audioSearchResults", query=query)

    return render(request, 'blog/audio.html')


def video(request):
    videos = Video.objects.all()
    return render(request, 'blog/video.html', context={'videos': videos[::-1]})


def audioSearchResults(request, query):
    validRequest = any(letter.isalpha() or letter.isspace()
                       for letter in query)
    if not validRequest:
        messages.add_message(request, messages.WARNING,
                             'Invalid Search')
        return redirect('blog-audio')
    results = []
    podcasts = Podcast.objects.all()
    for podcast in podcasts:
        if query.lower() in str(podcast).lower():
            results.append(podcast)
    if len(results) > 24:
        results = results[:24]
    return render(request, 'blog/audioResults.html', context={'podcasts': results, 'query': query, 'length': len(results)})


def downloads(request):
    context = {'pdfs': PDF.objects.all()[::-1]}
    return render(request, 'blog/pdfs.html', context=context)


class Blog(ListView):
    model = Post
    template_name = 'blog/posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 9


def tagDetails(request, _tag):
    try:
        tag = PostTag.objects.filter(title=_tag).first()
        context = {"tag": tag}
        return render(request, 'blog/tagdetails.html', context=context)
    except:
        return HttpResponse("That tag doesn't exist ):")
