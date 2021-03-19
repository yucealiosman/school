import factory
from django.contrib.auth import get_user_model

from school.unit import models


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: f"super_username_{n}")
    is_superuser = True
    is_staff = True


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: f"username_{n}")


class ClassRoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ClassRoom

    code = factory.Sequence(lambda n: f"code_{n}")

    @factory.post_generation
    def teachers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for teacher in extracted:
                self.teachers.add(teacher)


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Student

    username = factory.Sequence(lambda n: f"student_username_{n}")
    first_name = factory.Sequence(lambda n: f"student_name_{n}")
    number = factory.Sequence(lambda n: n)
    email = factory.Sequence(lambda n: f"mail_{n}@com")
    class_room = factory.Iterator(models.ClassRoom.objects.all())


class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Teacher

    username = factory.Sequence(lambda n: f"teacher_username_{n}")
    first_name = factory.Sequence(lambda n: f"teacher_name_{n}")

    @factory.post_generation
    def class_rooms(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for class_room in extracted:
                self.class_rooms.add(class_room)


class ClassHomeWorkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ClassHomeWork

    title = factory.Sequence(lambda n: f"title_{n}")
    description = factory.Sequence(lambda n: f"description_{n}")
    teacher = factory.SubFactory(TeacherFactory)
    class_room = factory.SubFactory(ClassRoomFactory)
