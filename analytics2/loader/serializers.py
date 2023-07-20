from rest_framework.serializers import Serializer
from rest_framework import serializers
from .models import DataFile, Project


class DataFileSerializer(serializers.HyperlinkedModelSerializer):
    file_name = serializers.CharField(read_only=True)
    file_type = serializers.CharField(read_only=True)
    size = serializers.CharField(read_only=True)
    project_fk = serializers.PrimaryKeyRelatedField(queryset=Project.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['project_fk'].queryset = Project.objects.filter(owner__groups__in=user.groups.all())

    class Meta:
        model = DataFile
        fields = '__all__'
    
    def create(self, validated_data):
        print("Validated_data:",str(validated_data))
        datafile = DataFile(
            file = validated_data['file'],
            file_name = validated_data['file'].name,
            file_type = validated_data['file'].content_type,
            size = validated_data['file'].size,
            description = validated_data['description'],
            project_fk = validated_data['project_fk'],
            status = validated_data['status'],
            year_quarter = validated_data['year_quarter'],
            file_mappings = validated_data['file_mappings']
        )
        datafile.save()
        return datafile
    

class DataFileDetailSerializer(serializers.HyperlinkedModelSerializer):
    file_name = serializers.CharField(read_only=True)
    file_type = serializers.CharField(read_only=True)
    size = serializers.CharField(read_only=True)

    class Meta:
        model = DataFile
        fields = '__all__'

 

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    datafiles = serializers.HyperlinkedRelatedField(many=True, view_name='datafile-detail', read_only=True)

    class Meta:
        model = Project
        fields = ('url', 'id', 'customer_name', 'project_id', 'datafiles', 'owner')