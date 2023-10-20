from rest_framework import generics
from .models import *
from .serializers import *
from .permissions import *
from rest_framework.response import Response
from django.db import connection
from django.db.models import Avg
from django.http import JsonResponse

class StudentAverageGradeView(generics.RetrieveAPIView):
    serializer_class = AverageGradeByStudentSerializer
    permission_classes = [isSelfReportAccessAllowed]
    def get_queryset(self):
        student_id = self.kwargs.get('pk')
        return Grade.objects.filter(student_id=student_id).values(
            'student__full_name', 'student__group__group', 'subject__subject'
        ).annotate(average_grade=Avg('grade')).order_by('-student__group__group', 'student__full_name', 'subject__subject')

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = AverageGradeByStudentSerializer(queryset, many=True)
        return Response(serializer.data)
    

class GroupAverageGradeView(generics.RetrieveAPIView):
    permission_classes = [IsReportGroupAccessAllowed]
    @staticmethod
    def dictfetchall(cursor):
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get(self, request, pk, *args, **kwargs):
        sql = """
            SELECT g."group", s.subject, AVG(gg.grade) as average_grade
            FROM api_group g
            JOIN api_group_subjects gs ON g.id = gs.group_id
            JOIN api_subject s ON gs.subject_id = s.id
            LEFT JOIN api_grade gg ON gg.subject_id = s.id
            WHERE g.id = %s
            GROUP BY g."group", s.subject;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [pk])
            avg_grades = self.dictfetchall(cursor)

        return JsonResponse(avg_grades, safe=False)


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from .serializers import UserSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from .serializers import UserSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from .serializers import UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


