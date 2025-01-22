from .views import JobList, JobDetail
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("jobs", JobList.as_view(), name="job_list"),
    path("jobs/<int:pk>", JobDetail.as_view(), name="job_detail"),
    # OpenAPI Schema:
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # OpenAPI UI:
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
