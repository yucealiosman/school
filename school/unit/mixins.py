class ServiceViewSetMixin:
    service_class = None

    def perform_create(self, serializer):
        instance = serializer.save()
        instance = self.service_class().create(instance)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        instance = self.service_class().update(instance)
        return instance

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance = self.service_class().delete(instance)
        return instance
