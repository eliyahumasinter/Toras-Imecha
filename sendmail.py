import threading
from django.core.mail import send_mail, send_mass_mail


class SendMassEmail(threading.Thread):

    def __init__(self, subject: str, message: str, recipient_list: list):
        self.subject = subject
        self.message = message
        self.recipient_list = list(recipient_list)
        self.messages = [(self.subject, message, 'rebecca@torasimecha.com', [recipient]) for recipient in recipient_list]
        threading.Thread.__init__(self)

    def run(self):
        send_mass_mail(self.messages)
        


class SendEmail(threading.Thread):

    def __init__(self, subject: str, message: str, recipient: str):
        self.subject = subject
        self.message = message
        self.recipient = recipient
        threading.Thread.__init__(self)

    def run(self):
        print("sending message")
        send_mail(self.subject, self.message, 'rebecca@torasimecha.com', ['rmasinter@gmail.com', 'eliyahumasinter@gmail.com'], fail_silently=False)

        