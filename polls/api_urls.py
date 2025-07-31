from django.urls import path
from .api_views import (
    QuestionListCreateAPIView,
    QuestionDetailAPIView,
    VoteAPIView,
    ResultAPIView,
    VoteTrendsAPIView,
)

urlpatterns = [
    path('questions/', QuestionListCreateAPIView.as_view(), name='api-question-list'),
    path('questions/<int:question_id>/', QuestionDetailAPIView.as_view(), name='api-question-detail'),
    path('questions/<int:question_id>/vote/', VoteAPIView.as_view(), name='api-vote'),
    path('questions/<int:question_id>/results/', ResultAPIView.as_view(), name='api-question-results'),
    path('questions/<int:question_id>/vote-trends/', VoteTrendsAPIView.as_view(), name='vote-trends'),
]

