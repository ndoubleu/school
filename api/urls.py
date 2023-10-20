from django.urls import path
from .views import *

urlpatterns = [
    path('reports/student/<int:pk>/', StudentAverageGradeView.as_view()),
    path('reports/group/<int:pk>/', GroupAverageGradeView.as_view(), name='average-grade-by-group'),
]
