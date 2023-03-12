from django.db.models.signals import post_save
from .models import Post, Podcast, PDF, Notification
from django.dispatch import receiver
from sendmail import SendMassEmail


@receiver(post_save, sender=Post)
def sendPostNotification(sender, instance, created, **kwargs):
    if created:
        peopleToNotify = Notification.objects.all()
        completeMessage = f"""A new post, {instance.title}, has been uploaded to Toras Imecha. \nYou can view it at https://torasimecha.com/posts/"""
        try:
            SendMassEmail("New Content on Toras Imecha!",
                      completeMessage, peopleToNotify).start()
        except Exception as e:
            print("Could not send email out from sendPostNotification", e)


@receiver(post_save, sender=Podcast)
def sendPodcastNotification(sender, instance, created, **kwargs):
    if created:
        peopleToNotify = Notification.objects.all()
        completeMessage = f"""A new podcast has been uploaded to Toras Imecha. \nYou can listen to it at https://torasimecha.com/"""
        try:
            SendMassEmail("New Content on Toras Imecha!",
                      completeMessage, peopleToNotify).start()
        except Exception as e:
            print("Could not send email out from sendPodcastNotification", e)


@receiver(post_save, sender=PDF)
def sendPDFNotification(sender, instance, created, **kwargs):
    if created:
        peopleToNotify = Notification.objects.all()
        completeMessage = f"""A new PDF Article, {instance.title}, has been uploaded to Toras Imecha. \nYou can view it at https://torasimecha.com/pdfs/"""
        try:
            SendMassEmail("New Content on Toras Imecha!",
                      completeMessage, peopleToNotify).start()
        except Exception as e:
                print("Could not send email out from sendPDFNotification", e)
