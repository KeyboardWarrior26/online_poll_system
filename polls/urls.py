from .views import health_check
from .api_views import VoteTrendsAPIView
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
    path('health/', views.health_check, name='health-check'),


    # Traditional HTML views (optional)
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),

    # REST API endpoints
    path('questions/', QuestionListCreateAPIView.as_view(), name='api-question-list'),
    path('questions/<int:question_id>/', QuestionDetailAPIView.as_view(), name='api-question-detail'),
    path('questions/<int:question_id>/vote/', VoteAPIView.as_view(), name='api-vote'),
    path('questions/<int:question_id>/results/', ResultAPIView.as_view(), name='api-question-results'),
    path('questions/<int:question_id>/vote-trends/', VoteTrendsAPIView.as_view(), name='vote-trends'),
]

