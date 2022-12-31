from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("profile", views.EmployerProfileViewSet, basename="employer-profile")

urlpatterns = router.urls
