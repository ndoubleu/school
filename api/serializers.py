from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('student', 'subject', 'grade')

class AverageGradeByStudentSerializer(serializers.Serializer):
    full_name = serializers.CharField(source='student__full_name') 
    group = serializers.CharField(source='student__group__group')  
    subject = serializers.CharField(source='subject__subject')
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
        fields = ('id', 'username', 'is_director', 'is_student', 'is_teacher', 'full_name', 'group')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user or self.context['request'].user
        user_serializer = UserSerializer(user)
        data['user'] = user_serializer.data

        return data