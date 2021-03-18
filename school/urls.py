from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_extensions.routers import ExtendedDefaultRouter

from school.unit.urls import router as unit_router

schema_view = get_schema_view(
    openapi.Info(
        title="School API",
        default_version='v1',
        description="School Application API",
        contact=openapi.Contact(email="aliosmanyuce@gmail.com")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = ExtendedDefaultRouter()
router.registry.extend(unit_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/v1/', include(router.urls)),
    path(r'api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path(r'api/v1/docs/json/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
]
