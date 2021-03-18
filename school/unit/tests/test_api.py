import json
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from school.unit import models
from school.unit.tests import factories
from school.unit.tests.factories import SuperUserFactory


class BaseTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=SuperUserFactory())


class StudentApiTest(BaseTest):
    def test_student_list(self):
        student_count = 5
        teacher = factories.TeacherFactory()
        class_room = factories.ClassRoomFactory(teachers=[teacher])
        student_list = factories.StudentFactory.create_batch(
            class_room=class_room, size=student_count)

        expected_student_pk_set = {str(student.pk) for student in
                                   student_list}

        response = self.client.get(reverse('students-list'))
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         response.data)
        self.assertEqual(data['count'], student_count)
        student_pk_set_from_resp = {student["pk"] for student in
                                    data["results"]}
        self.assertEqual(expected_student_pk_set, student_pk_set_from_resp)

    def test_student_detail(self):
        teacher = factories.TeacherFactory()
        class_room = factories.ClassRoomFactory(teachers=[teacher])
        student = factories.StudentFactory(class_room=class_room)

        response = self.client.get(
            reverse('students-detail', kwargs={'pk': str(student.pk)}))
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         response.data)
        data = response.json()
        self.assertEqual(class_room.code, data["class_room"]["code"])
        teacher_pk_list_from_resp = [teacher["pk"] for teacher in
                                     data["class_room"]["teachers"]]
        self.assertEqual(teacher_pk_list_from_resp, [str(teacher.pk)])


class HomeWorkApiTest(BaseTest):
    @patch('school.unit.services.HomeWorkService.notify')
    def test_create_homework(self, notify_mock):
        teacher = factories.TeacherFactory()
        class_room = factories.ClassRoomFactory(teachers=[teacher])

        hw_not_created = factories.ClassHomeWorkFactory.build()
        data = {
            'title': hw_not_created.title,
            'description': hw_not_created.description,
            'class_room': str(class_room.pk)
        }
        response = self.client.post(
            reverse('homeworks-by-teacher-list',
                    kwargs={'teacher__pk': str(teacher.pk)}),
            data=json.dumps(data),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         response.data)
        data = response.json()
        hw_created = models.ClassHomeWork.objects.get(pk=data["pk"])

        self.assertEqual(data["title"], hw_not_created.title)
        self.assertEqual(data["description"], hw_not_created.description)
        self.assertEqual(data["teacher"], str(teacher.pk))
        self.assertEqual(data["class_room"], str(class_room.pk))
        notify_mock.assert_called_once_with(hw_created, 'created')

    @patch('school.unit.services.HomeWorkService.notify')
    def test_update_homework(self, notify_mock):
        teacher = factories.TeacherFactory()
        class_room = factories.ClassRoomFactory(teachers=[teacher])

        homework = factories.ClassHomeWorkFactory(class_room=class_room,
                                                  teacher=teacher)

        new_description = "New HomeWork description"
        update_data = {
            'description': new_description
        }
        response = self.client.patch(
            reverse('homeworks-by-teacher-detail',
                    kwargs={'teacher__pk': str(teacher.pk),
                            'pk': str(homework.pk)}),
            data=json.dumps(update_data),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         response.data)
        data = response.json()
        self.assertEqual(data["description"], new_description)
        notify_mock.assert_called_once_with(homework, 'updated')

    @patch('school.unit.services.HomeWorkService.notify')
    def test_delete_homework(self, notify_mock):
        homework = factories.ClassHomeWorkFactory()
        response = self.client.delete(
            reverse('homeworks-by-teacher-detail',
                    kwargs={'teacher__pk': str(homework.teacher.pk),
                            'pk': str(homework.pk)}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                         response.data)
        self.assertFalse(
            models.ClassHomeWork.objects.filter(pk=homework.pk).exists())
        notify_mock.assert_called_once()
