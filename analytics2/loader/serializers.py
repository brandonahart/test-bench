from rest_framework.serializers import Serializer
from rest_framework import serializers
from .models import DataFile, Project


class DataFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    file_name = serializers.CharField(read_only=True)
    file_type = serializers.CharField(read_only=True)
    size = serializers.CharField(read_only=True)

    class Meta:
        model = DataFile
        fields = '__all__'
    
    def create(self, validated_data):
        print("Validated_data:",str(validated_data))
        datafile = DataFile(
            file_name = validated_data['file'].name,
            file_type = validated_data['file'].content_type,
            size = validated_data['file'].size,
            description = validated_data['description'],
            project_fk = validated_data['project_fk'],
            status = validated_data['status'],
            year_quarter = validated_data['year_quarter']
        )
        datafile.save()
        return datafile
 

class ProjectSerializer(serializers.ModelSerializer):

    datafiles = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'customer_name', 'project_id', 'datafiles')