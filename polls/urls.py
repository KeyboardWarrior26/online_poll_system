from django.urls import path
from . import views
from .api_views import (
    QuestionListCreateAPIView,
    QuestionDetailAPIView,
    VoteAPIView,
    ResultAPIView,
)

app_name = 'polls'

urlpatterns = [
    # HTML views (if needed later)
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),

    # REST API (no "api/" prefix here)
    path('questions/', QuestionListCreateAPIView.as_view(), name='api-question-list'),
    path('questions/<int:pk>/', QuestionDetailAPIView.as_view(), name='api-question-detail'),
    path('questions/<int:question_id>/vote/', VoteAPIView.as_view(), name='api-vote'),
    path('questions/<int:question_id>/results/', ResultAPIView.as_view(), name='api-question-results'),
]

