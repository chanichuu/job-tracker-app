from .views import JobList, JobDetail
from django.urls import path


urlpatterns = [
    path("jobs", JobList.as_view(), name="job_list"),
    path("jobs/<int:pk>/", JobDetail.as_view(), name="job_detail"),
]
