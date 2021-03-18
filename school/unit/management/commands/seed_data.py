import logging

from django.core.management.base import BaseCommand

from school.unit.tests import factories

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Create sample model instances'

    def add_arguments(self, parser):
        parser.add_argument('student_per_class', type=int)
        parser.add_argument('teacher_count', type=int)

    def handle(self, *args, **options):
        # Every class room has 2 two teacher, every teach has 1 homework.
        logger.info("Data seeding started")

        student_per_class = options.get('student_per_class', 5)
        class_room_count = options.get('class_room_count', 3)

        class_rooms = factories.ClassRoomFactory.create_batch(class_room_count)

        for class_room in class_rooms:
            teacher_list = factories.TeacherFactory.create_batch(
                2, class_rooms=[class_room])
            factories.ClassHomeWorkFactory(
                teacher=teacher_list[0], class_room=class_room)
            factories.ClassHomeWorkFactory(
                teacher=teacher_list[1], class_room=class_room)

            factories.StudentFactory.create_batch(
                student_per_class, class_room=class_room)

        logger.info("Data seeding finished")
