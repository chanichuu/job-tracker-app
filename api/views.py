from django.http import Http404
from rest_framework import status, generics
from .serializers import JobSerializer, UserSerializer
from django.contrib.auth.models import User
from .models import Job
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .mixins import LoggingMixin
from rest_framework.permissions import AllowAny


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class JobList(LoggingMixin, APIView):
    """
    List all jobs, or create a new job.
    """

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="state",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Filter by job state. Valid values: NEW, APPLIED, INTERVIEW, REJECTED, OFFER",
                required=False,
            ),
            OpenApiParameter(
                name="priority",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter by priority. Valid values: 1, 2, 3",
            ),
            OpenApiParameter(
                name="isFavourite",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Filter all favourites. Valid values: True, False",
            ),
        ],
        responses={200: JobSerializer(many=True), 401: None},
        methods=["GET"],
        description="Get all jobs or jobs filtered by state, priority or favourites.",
    )
    def get(self, request, format=None):
        state = self.request.query_params.get("state")
        priority = self.request.query_params.get("priority")
        is_favourite = self.request.query_params.get("isFavourite")
        jobs = Job.objects.filter(user=request.user)

        if state:
            jobs = jobs.filter(state=state)
        if priority:
            jobs = jobs.filter(priority=priority)
        if is_favourite:
            jobs = jobs.filter(is_favourite=is_favourite)
        serializer = JobSerializer(jobs, many=True)

        return Response(serializer.data)

    @extend_schema(
        request=JobSerializer,
        responses={201: JobSerializer, 400: None, 401: None, 404: None},
        methods=["POST"],
        description="Create a new job.",
    )
    def post(self, request, format=None):
        serializer = JobSerializer(data=request.data)
        user = request.user
        if user is None:
            return Response(
                {"Unauthorized:": "No valid user found"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if serializer.is_valid():
            serializer.validated_data["user"] = user

            queryset = Job.objects.filter(
                job_name=serializer.validated_data.get("job_name"),
                company_name=serializer.validated_data.get("company_name"),
                user=serializer.validated_data.get("user"),
            )
            if queryset.exists():
                return Response(
                    {"Bad Request:": "Job already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobDetail(LoggingMixin, APIView):
    """
    Retrieve, update or delete a job instance.
    """

    def get_object(self, pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise Http404

    @extend_schema(
        responses={200: JobSerializer, 401: None, 404: None},
        methods=["GET"],
        description="Get a job by id.",
    )
    def get(self, request, pk, format=None):
        job = self.get_object(pk)
        if job.user != request.user:
            return Response(
                {"Forbidden:": "Job not accessible."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = JobSerializer(job)

        return Response(serializer.data)

    @extend_schema(
        request=JobSerializer,
        responses={200: JobSerializer, 400: None, 401: None, 404: None},
        methods=["PUT"],
        description="Update a job by id.",
    )
    def put(self, request, pk, format=None):
        job = self.get_object(pk)
        if job.user != request.user:
            return Response(
                {"Forbidden:": "Job not accessible."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            queryset = Job.objects.filter(id=pk)

            if queryset.exists():
                if queryset[0].job_name != serializer.validated_data.get(
                    "job_name"
                ) or queryset[0].company_name != serializer.validated_data.get(
                    "company_name"
                ):
                    return Response(
                        {"Bad Request:": "Job and company name cannot be updated."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            204: None,
            401: {"detail": "Authentication credentials were not provided."},
            404: None,
        },
        methods=["DELETE"],
        description="Delete a job by id.",
    )
    def delete(self, request, pk, format=None):
        job = self.get_object(pk)
        if job.user != request.user:
            return Response(
                {"Forbidden:": "Job not accessible."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if job.address:
            job.address.delete()
        if job.contact:
            job.contact.delete()
        job.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
