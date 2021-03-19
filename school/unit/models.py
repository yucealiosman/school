import uuid
from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import deletion


class UserType(Enum):
    STUDENT = "Student"
    TEACHER = "Teacher"


USER_TYPES = [(choice.name, choice.value) for choice in UserType]


class BaseModel(models.Model):
    uuid = models.UUIDField(editable=False, help_text="Unique ID",
                            primary_key=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.pk = uuid.uuid4()
        return super().save(*args, **kwargs)


class Notification(BaseModel):
    text = models.CharField(max_length=64)
    sender = models.ForeignKey("User", related_name="sent_notifications",
                               on_delete=deletion.CASCADE)
    receiver = models.ForeignKey("User", related_name="received_notifications",
                                 on_delete=deletion.CASCADE)

    is_read = models.BooleanField(default=False)


class User(BaseModel, AbstractUser):
    def __str__(self):
        return f"{self.first_name} - {self.last_name}"


class Student(User):
    number = models.CharField(max_length=32, unique=True)
    class_room = models.ForeignKey("ClassRoom", related_name='students',
                                   on_delete=deletion.SET_NULL,
                                   null=True, blank=True)

    def save(self, *args, **kwargs):
        self.type = UserType.STUDENT.name
        super().save(*args, **kwargs)


class Teacher(User):
    def save(self, *args, **kwargs):
        self.type = UserType.TEACHER.name
        super().save(*args, **kwargs)


class ClassRoom(BaseModel):
    code = models.CharField(max_length=32, unique=True)
    teachers = models.ManyToManyField("Teacher", related_name="class_rooms")

    def __str__(self):
        return self.code


class ClassHomeWork(BaseModel):
    title = models.CharField(max_length=64, null=True)
    description = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=deletion.CASCADE,
                                related_name="home_works")
    class_room = models.ForeignKey(ClassRoom, on_delete=deletion.CASCADE,
                                   related_name="home_works")

    def __str__(self):
        return self.title
