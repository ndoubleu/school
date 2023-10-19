from rest_framework import serializers
from .models import *

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('student', 'subject', 'grade')

class AverageGradeByStudentSerializer(serializers.Serializer):
    full_name = serializers.CharField(source='student.name')
    group = serializers.CharField(source='student.group.name')
    subject = serializers.CharField(source='subject.name')
    average_grade = serializers.FloatField()

class AverageGradeByGroupSerializer(serializers.Serializer):
    group = serializers.CharField()
    subject = serializers.CharField()
    average_grade = serializers.FloatField()

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True)
    class Meta:
        model = Group
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'