from unittest.mock import patch

from django.test import TestCase

from school.unit import notification
from school.unit.tests import factories


class TeacherEmailTest(TestCase):
    @patch('school.unit.notification.send_homework_mail.apply_async')
    def test_send_func(self, email_mock):
        teacher = factories.TeacherFactory()
        classroom = factories.ClassRoomFactory(teachers=[teacher])
        student = factories.StudentFactory(class_room=classroom)
        factories.StudentFactory(
            class_room=factories.ClassRoomFactory())
        hw = factories.ClassHomeWorkFactory(teacher=teacher,
                                            class_room=classroom)
        action = student
        expected_email_list = [student.email]

        notification.TeacherHomeworkEmailAdapter().send(home_work=hw,
                                                        action=action)

        email_mock.assert_called_once_with(args=[expected_email_list, hw.title,
                                           action], kwargs={})


class TeacherPushNotificationTest(TestCase):
    @patch(
        'school.unit.notification.send_homework_push_notification.apply_async')  # noqa
    def test_send_func(self, push_notify_mock):
        hw = factories.ClassHomeWorkFactory()
        action = 'created'
        notification.TeacherHomeworkPushNotificationAdapter().send(
            home_work=hw,
            action=action)
        push_notify_mock.assert_called_once_with(args=[], kwargs={})
