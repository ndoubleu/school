from django.urls import path
from .views import *

urlpatterns = [
    path('reports/student/<int:pk>/', StudentAverageGradeView.as_view()),
    path('reports/group/<int:pk>/', GroupAverageGradeView.as_view(), name='average-grade-by-group'),

    # path('subjects/', SubjectLC.as_view(), name='subject-list-create'),
    # path('subjects/<int:pk>/', SubjectRUDA.as_view(), name='subject-retrieve-update-delete'),

    # path('groups/', GroupLC.as_view(), name='group-list-create'),
    # path('groups/<int:pk>/', GroupRUDA.as_view(), name='group-retrieve-update-delete'),

    # path('users/', UserLC.as_view(), name='user-list-create'),
    # path('users/<int:pk>/', UserRUDA.as_view(), name='user-retrieve-update-delete'),
]
