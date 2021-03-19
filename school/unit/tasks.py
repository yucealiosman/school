from django.conf import settings
from django.core.mail import send_mail

from school.unit.celery import app
from school.unit.models import Notification, User


@app.task
def send_homework_mail(student_mail_list, title, action):
    # We can also use celery-email-backend instead of using this function
    send_mail(
        subject="New Homework!",
        message=f"{title} is {action}",
        from_email=settings.DEFAULT_EMAIL_FROM,
        recipient_list=student_mail_list,
        fail_silently=False)


@app.task
def send_homework_push_notification(receiver_pk_list, sender_pk, title, action):
    receivers = User.objects.filter(pk__in=receiver_pk_list)
    sender = User.objects.get(pk=sender_pk)
    text = f"{title}, {action}"
    [Notification.objects.create(sender=sender, receiver=student, text=text)
     for student in receivers]
