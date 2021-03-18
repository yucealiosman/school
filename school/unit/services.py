from typing import List

from django.conf import settings
from django.utils.functional import cached_property

from school.unit.notification import (
    TeacherHomeworkEmailAdapter, TeacherHomeworkPushNotificationAdapter,
    NotificationAdapter)


class BaseService:
    def create(self, instance):
        return instance

    def update(self, instance):
        return instance

    def delete(self, instance):
        return instance


class NotificationService(BaseService):
    @cached_property
    def notification_systems(self) -> List[NotificationAdapter]:
        raise NotImplementedError

    def create(self, instance):
        self._notify(instance, 'created')
        return super().create(instance)

    def update(self, instance):
        self._notify(instance, 'updated')
        return super().update(instance)

    def delete(self, instance):
        self._notify(instance, 'deleted')
        return super().delete(instance)

    def _notify(self, instance, action):
        if settings.NOTIFY:
            self.notify(instance, action)

    def notify(self, instance, action):
        for notification_system in self.notification_systems:
            notification_system.send(instance, action)


class HomeWorkService(NotificationService):
    @cached_property
    def notification_systems(self):
        return [TeacherHomeworkEmailAdapter(),
                TeacherHomeworkPushNotificationAdapter()]
