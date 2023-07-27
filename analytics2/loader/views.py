from django.shortcuts import render
from rest_framework import status, generics
from rest_framework import filters
from .serializers import DataFilDetailSerializer, DataFileSerializer, ProjectSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view


from loader.models import DataFile, Project

# Create your views here.
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'projects': reverse('project-list', request=request, format=format),
        #'datafiles': reverse('datafile-list', request=request, format=format)
    })

class DataFileAPIView(generics.ListCreateAPIView):
    queryset = DataFile.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = DataFileSerializer
    
    def get_queryset(self):
        '''
        queryset = DataFile.objects.all()
        project = self.request.query_params.get('project')
        period = self.request.query_params.get('period')
        if project and period:
            queryset = queryset.filter(project_fk=project,year_quarter__contains=period)
        elif project:
            queryset = queryset.filter(project_fk=project)
        elif period:
            queryset = queryset.filter(year_quarter__contains=period)
        return queryset
        '''
        project_fk = self.kwargs['project_fk']
        year_quarter = self.kwargs['year_quarter']
        return DataFile.objects.filter(project_fk__project_id=project_fk, year_quarter=year_quarter)



class DataFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DataFile.objects.all()
    serializer_class = DataFilDetailSerializer


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectDetail(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Include data files grouped by year-quarter in the response
        data_files = DataFile.objects.filter(project_fk=instance.project_id).values_list('year_quarter', flat=True).distinct()
        print(data_files)
        data_file_urls = {
            year_quarter: request.build_absolute_uri(reverse('datafile-list', kwargs={'project_fk': instance.project_id, 'year_quarter': year_quarter}))
            for year_quarter in data_files
        }
        response_data = serializer.data
        response_data['data_file_urls'] = data_file_urls
        
        return Response(response_data)