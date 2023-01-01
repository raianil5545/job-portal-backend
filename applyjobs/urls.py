from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("", views.ApplyJobViewSet, basename="apply-job")

urlpatterns = router.urls
