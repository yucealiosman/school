from abc import ABC, abstractmethod

from school.unit.tasks import (send_homework_mail,
                               send_homework_push_notification)
from school.unit.models import Student


class NotificationAdapter(ABC):
    @abstractmethod
    def send(self, instance, action):
        pass


class TeacherHomeworkEmailAdapter(NotificationAdapter):
    def send(self, home_work, action):
        student_mail_list = list(Student.objects.filter(
            class_room=home_work.class_room).values_list("email", flat=True))
        title = home_work.title

        send_homework_mail.apply_async(args=[student_mail_list, title, action],
                                       kwargs={})


class TeacherHomeworkPushNotificationAdapter(NotificationAdapter):
    def send(self, home_work, action):
        send_homework_push_notification.apply_async(args=[],
                                                    kwargs={})
