from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from .serializers import JobSerializer
from .models import Job
from rest_framework.views import APIView
from rest_framework.response import Response


class JobList(APIView):
    """
    List all jobs, or create a new job.
    """

    def get(self, request, format=None):
        state = self.request.query_params.get("state")
        priority = self.request.query_params.get("priority")
        jobs = Job.objects.all()

        if state:
            jobs = jobs.filter(state=state)
        if priority:
            jobs = jobs.filter(priority=priority)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            queryset = Job.objects.filter(
                job_name=serializer.validated_data.get("job_name"),
                company_name=serializer.validated_data.get("company_name"),
            )
            if queryset.exists():
                return Response(
                    {"Bad Request:": "Job already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobDetail(APIView):
    """
    Retrieve, update or delete a job instance.
    """

    def get_object(self, pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        job = self.get_object(pk)
        serializer = JobSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        job = self.get_object(pk)
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            queryset = Job.objects.filter(
                job_name=serializer.validated_data.get("job_name"),
                company_name=serializer.validated_data.get("company_name"),
            )
            if queryset.exists() and queryset[0].id != pk:
                return Response(
                    {"Bad Request:": "Job already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        job = self.get_object(pk)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
