from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("profile", views.ApplicantProfileViewSet, basename="profile")

urlpatterns = router.urls
