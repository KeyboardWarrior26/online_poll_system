from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status, filters
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.utils import timezone
from django.db.models.functions import TruncDay, TruncWeek

from .models import Question, Choice, Vote
from .serializers import (
    QuestionSerializer,
    QuestionCreateSerializer,
    QuestionResultSerializer,
)


class QuestionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class QuestionListCreateAPIView(ListCreateAPIView):
    queryset = Question.objects.all()
    pagination_class = QuestionPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['question_text']
    ordering_fields = ['pub_date']
    ordering = ['-pub_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        status_param = self.request.query_params.get('status')

        if status_param == 'active':
            queryset = queryset.filter(
                Q(expiry_date__gt=timezone.now()) | Q(expiry_date__isnull=True)
            )
        elif status_param == 'expired':
            queryset = queryset.filter(expiry_date__lte=timezone.now())

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuestionCreateSerializer
        return QuestionSerializer


class QuestionDetailAPIView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_url_kwarg = 'question_id'


class VoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, question_id):
        user = request.user
        question = get_object_or_404(Question, pk=question_id)
        choice_id = request.data.get('choice_id')

        if not choice_id:
            return Response(
                {"error": "The 'choice_id' field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            choice = Choice.objects.get(pk=choice_id, question=question)
        except Choice.DoesNotExist:
            return Response(
                {"error": "Invalid choice for this question."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Vote.objects.filter(user=user, choice__question=question).exists():
            return Response(
                {"error": "You have already voted for this question."},
                status=status.HTTP_403_FORBIDDEN
            )

        Vote.objects.create(user=user, choice=choice)
        return Response({"message": "Vote counted."}, status=status.HTTP_201_CREATED)


class ResultAPIView(APIView):
    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        choices = question.choices.annotate(vote_count=Count('votes'))
        total_votes = sum(c.vote_count for c in choices) or 0

        results = []
        for choice in choices:
            percentage = (
                round((choice.vote_count / total_votes) * 100, 2) if total_votes > 0 else 0
            )
            results.append({
                "id": choice.id,
                "choice_text": choice.choice_text,
                "votes": choice.vote_count,
                "percentage": percentage,
            })

        return Response({
            "question": question.question_text,
            "total_votes": total_votes,
            "results": results
        })


class VoteTrendsAPIView(APIView):
    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        period = request.query_params.get('period', 'day')  # default to 'day'

        if period == 'week':
            trunc_func = TruncWeek
        else:
            trunc_func = TruncDay

        votes = (
            Vote.objects
            .filter(choice__question=question)
            .annotate(period=trunc_func('voted_at'))
            .values('period')
            .annotate(count=Count('id'))
            .order_by('period')
        )

        data = [{"period": v['period'].date(), "votes": v['count']} for v in votes]

        return Response({
            "question": question.question_text,
            "period": period,
            "vote_trends": data
        })

