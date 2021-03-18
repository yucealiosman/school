from rest_framework_extensions.routers import ExtendedDefaultRouter

from school.unit import views

router = ExtendedDefaultRouter()

teacher_router = router.register(r'teachers', views.TeacherViewSet,
                                 basename='teachers')

teacher_router.register(r'homeworks', views.HomeWorkNestedViewSet,
                        basename='homeworks-by-teacher',
                        parents_query_lookups=['teacher__pk'])

student_router = router.register(r'students', views.StudentViewSet,
                                 basename='students')
