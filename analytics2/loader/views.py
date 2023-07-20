from django.shortcuts import render, HttpResponse
from rest_framework import status, generics
from .serializers import DataFileDetailSerializer, DataFileSerializer, ProjectSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from django.contrib.auth.models import Group
from rest_framework import permissions


from loader.models import DataFile, Project

# Create your views here.
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'projects': reverse('project-list', request=request, format=format),
        'datafiles': reverse('datafile-list', request=request, format=format)
    })

class DataFileAPIView(generics.ListCreateAPIView):
    queryset = DataFile.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = DataFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):    
        if self.request.user.is_staff:
            queryset = DataFile.objects.all()
        else:
            queryset = DataFile.objects.all().filter(project_fk__owner__groups__in=self.request.user.groups.all())
        project = self.request.query_params.get('project')
        period = self.request.query_params.get('period')

        if project and period:
            queryset = queryset.filter(project_fk=project,year_quarter__contains=period)
        elif project:
            queryset = queryset.filter(project_fk=project)
        elif period:
            queryset = queryset.filter(year_quarter__contains=period)

        return queryset


class DataFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DataFile.objects.all()
    serializer_class = DataFileDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not Group.objects.filter(name=self.request.data.get('project_id')).exists():
            g1 = Group.objects.create(name=self.request.data.get('project_id'))
            g1.user_set.add(self.request.user)  # Add the current user to the group
        else:
            g1 = Group.objects.get(name=self.request.data.get('project_id'))
            g1.user_set.add(self.request.user)  # Add the current user to the group

        serializer.save(owner=self.request.user)

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return Project.objects.all()
        else:
            return Project.objects.all().filter(owner__groups__in=self.request.user.groups.all())
        #return Project.objects.all().filter(owner=self.request.user)

class ProjectDetail(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
