from rest_framework import serializers

from school.unit import models


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ('pk', )


class ClassHomeWorkNestedSerializer(BaseSerializer):
    class Meta:
        model = models.ClassHomeWork
        fields = ('pk', 'title', 'teacher', 'description', 'class_room')


class TeacherSerializer(BaseSerializer):
    class Meta:
        model = models.Teacher
        fields = ('pk', 'first_name')


class ClassRoomSerializer(BaseSerializer):
    teachers = TeacherSerializer(many=True)

    class Meta:
        model = models.ClassRoom
        fields = ('pk', 'code', 'teachers',)


class StudentSerializer(BaseSerializer):
    class_room = ClassRoomSerializer()

    class Meta:
        model = models.Student
        fields = ('pk', 'class_room', 'first_name', 'number', 'email')
