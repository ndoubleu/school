from rest_framework import generics
from .models import *
from .serializers import *
from .permissions import IsReportAccessAllowed
from rest_framework.response import Response
from django.db import connection
from django.db.models import Avg
class AverageGradeByStudentAPIView(generics.ListAPIView):
    serializer_class = AverageGradeByStudentSerializer
    permission_classes = [IsReportAccessAllowed]

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        return Grade.objects.filter(student_id=student_id).values('student__name', 'student__group__name', 'subject__name').annotate(average_grade=models.Avg('grade')).order_by('-student__group__name', 'student__name')

class AverageGradeByGroupAPIView(generics.ListAPIView):
    serializer_class = AverageGradeByGroupSerializer
    permission_classes = [IsReportAccessAllowed]

    def get_queryset(self):
        return Grade.objects.values('student__group__name', 'subject__name').annotate(average_grade=models.Avg('grade')).order_by('student__group__name')
    
# class SubjectLC(generics.ListCreateAPIView):
#     serializer_class = SubjectSerializer
#     queryset = Subject.objects.all()

# class SubjectRUDA(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = SubjectSerializer
#     queryset = Subject.objects.all()

# class GroupLC(generics.ListCreateAPIView):
#     serializer_class = GroupSerializer
#     queryset = Group.objects.all()

# class GroupRUDA(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = GroupSerializer
#     queryset = Group.objects.all()

# class UserLC(generics.ListCreateAPIView):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

# class UserRUDA(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

class StudentAverageGradeView(generics.RetrieveAPIView):
    serializer_class = GradeSerializer

    def retrieve(self, request, *args, **kwargs):
        student_id = kwargs.get('pk')
        average_grades = Grade.objects.filter(student_id=student_id).values('subject__subject', 'subject__day', 'subject__time').annotate(average_grade=Avg('grade')).order_by('-student__group', 'student__full_name')
        return Response(average_grades)
    
class GroupAverageGradeView(generics.RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        group_id = kwargs.get('pk')
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT g.group, s.subject, AVG(grade) as average_grade
                FROM api_grade AS g
                INNER JOIN api_subject AS s ON g.subject_id = s.id
                INNER JOIN api_user AS u ON g.student_id = u.id
                WHERE u.group_id = %s
                GROUP BY g.group, s.subject
                ORDER BY g.group, s.subject
            ''', [group_id])
            rows = cursor.fetchall()

        results = []
        for row in rows:
            group, subject, average_grade = row
            results.append({
                'group': group,
                'subject': subject,
                'average_grade': average_grade
            })

        return Response(results)
