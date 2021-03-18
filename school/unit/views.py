from django.db.models import Prefetch
from django.http import Http404
from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin

from school.unit import models
from school.unit import serializers
from school.unit.mixins import ServiceViewSetMixin
from school.unit.services import HomeWorkService


class NestedBaseViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    parent_field = None  # property that will be override at child class

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        params = self.get_parents_query_dict()
        if self.parent_field and hasattr(serializer, 'initial_data'):
            serializer.initial_data[self.parent_field] = params[
                f'{self.parent_field}__pk']
        return serializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer


class HomeWorkNestedViewSet(ServiceViewSetMixin, NestedBaseViewSet):
    service_class = HomeWorkService
    parent_field = 'teacher'
    queryset = models.ClassHomeWork.objects.all()
    serializer_class = serializers.ClassHomeWorkNestedSerializer


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.StudentSerializer

    def get_queryset(self):
        query_set = models.Student.objects.select_related(
            "class_room").prefetch_related(
            Prefetch(
                'class_room__teachers',
                queryset=models.Teacher.objects.only('name', 'uuid'),
            )
        )

        return query_set

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        query_set = models.Student.objects.filter(
            **filter_kwargs).select_related(
            "class_room").prefetch_related(
            Prefetch(
                'class_room__teachers',
                queryset=models.Teacher.objects.only('name', 'uuid'),
            )
        )

        if not query_set.exists():
            raise Http404

        obj = query_set[0]
        self.check_object_permissions(self.request, obj)

        return obj
