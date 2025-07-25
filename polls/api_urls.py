from .api_views import (
    QuestionListCreateAPIView,
    QuestionDetailAPIView,
    VoteAPIView,
    ResultAPIView,
)

urlpatterns = [
    path('api/questions/', QuestionListCreateAPIView.as_view(), name='api-question-list'),
    path('api/questions/<int:pk>/', QuestionDetailAPIView.as_view(), name='api-question-detail'),
    path('api/questions/<int:question_id>/vote/', VoteAPIView.as_view(), name='api-vote'),
    path('api/questions/<int:question_id>/results/', ResultAPIView.as_view(), name='api-question-results'),
]

