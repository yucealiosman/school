import uuid

from django.db import models
from django.db.models import deletion


class BaseModel(models.Model):
    uuid = models.UUIDField(editable=False, help_text="Unique ID",
                            primary_key=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.uuid is None:
            self.uuid = uuid.uuid4()
        return super().save(*args, **kwargs)


class Student(BaseModel):
    name = models.CharField(max_length=64)
    number = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=254)
    class_room = models.ForeignKey("ClassRoom", related_name='students',
                                   on_delete=deletion.SET_NULL,
                                   null=True, blank=True)

    def __str__(self):
        return f"{str(self.name)}"


class Teacher(BaseModel):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


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
