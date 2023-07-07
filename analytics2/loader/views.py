from django.shortcuts import render
from rest_framework import status, generics
from rest_framework import filters
from .serializers import DataFileSerializer, ProjectSerializer
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
        'datafiles': reverse('datafile-list', request=request, format=format)
    })

'''
class DataFileAPIView(APIView):
    queryset = DataFile.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = DataFileSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            uploaded_file = serializer.validated_data["file"]
            #function to write file somewhere

            serializer.save()
            print('DEBUG:',str(serializer.data))
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        
        datafiles = [datafile.file_name for datafile in DataFile.objects.all()]
        return Response(datafiles)
 '''  
class DataFileAPIView(generics.ListCreateAPIView):
    #search_fields = ['=project_fk__project_id','=year_quarter']
    #filter_backends = (filters.SearchFilter,)
    queryset = DataFile.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = DataFileSerializer
    
    def get_queryset(self):
        queryset = DataFile.objects.all()
        project = self.request.query_params.get('project')
        period = self.request.query_params.get('period')

        if project and period:
            queryset = queryset.filter(project_fk=project,year_quarter=period)
        elif project:
            queryset = queryset.filter(project_fk=project)
        elif period:
            queryset = queryset.filter(year_quarter=period)

        return queryset


class DataFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DataFile.objects.all()
    serializer_class = DataFileSerializer


#these two functions can be combined into a single function using viewsets instead of generics
class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectDetail(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer