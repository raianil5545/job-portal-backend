from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/user/", include("account.urls")),
    path("api/applicant/", include("applicant_profile.urls")),
    path("api/employer/", include("employer_profile.urls")),
    path("api/jobs/", include("job.urls")),
    path("api/job-posted/", include("applyjobs.urls")),
]
