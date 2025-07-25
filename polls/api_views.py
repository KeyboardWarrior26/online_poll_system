from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .models import Question, Choice, Vote
from .serializers import (
    QuestionSerializer,
    QuestionCreateSerializer,
    QuestionResultSerializer,
)


class QuestionDetailAPIView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_url_kwarg = 'question_id'  # This tells DRF to use question_id from URL


class QuestionListCreateAPIView(ListCreateAPIView):
    queryset = Question.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuestionCreateSerializer
        return QuestionSerializer


class VoteAPIView(APIView):
    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        choice_id = request.data.get('choice_id')

        if not choice_id:
            return Response(
                {"error": "choice_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            choice = Choice.objects.get(pk=choice_id, question=question)
        except Choice.DoesNotExist:
            return Response(
                {"error": "Invalid choice for this question."},
                status=status.HTTP_404_NOT_FOUND
            )

        Vote.objects.create(choice=choice)
        return Response({"message": "Vote counted."}, status=status.HTTP_201_CREATED)


class ResultAPIView(APIView):
    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)

        # Annotate vote counts
        choices = question.choices.annotate(vote_count=Count('votes'))
        total_votes = sum([c.vote_count for c in choices]) or 0

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

