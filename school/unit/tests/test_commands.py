from django.test import TestCase

from school.unit import models
from school.unit.management.commands.seed_data import Command


class SeedDataTest(TestCase):
    def test_seed_data_command(self):
        # Every class room has 2 two teacher, every teach has 1 homework.

        student_per_class = 5
        class_room_count = 4
        Command().handle(student_per_class=student_per_class,
                         class_room_count=class_room_count)

        self.assertEqual(models.ClassRoom.objects.count(), class_room_count)
        self.assertEqual(models.Student.objects.count(),
                         student_per_class * class_room_count)

        self.assertEqual(models.Teacher.objects.count(), 8)
        self.assertEqual(models.ClassHomeWork.objects.count(), 8)
