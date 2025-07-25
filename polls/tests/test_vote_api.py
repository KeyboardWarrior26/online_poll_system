from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from polls.models import Question, Choice
from django.utils import timezone

class VoteAPITestCase(APITestCase):
    def setUp(self):
        self.question = Question.objects.create(
            question_text="What's your favorite programming language?",
            pub_date=timezone.now()
        )
        self.choice1 = Choice.objects.create(
            question=self.question,
            choice_text="Python",
            votes=0
        )
        self.choice2 = Choice.objects.create(
            question=self.question,
            choice_text="JavaScript",
            votes=0
        )
        self.vote_url = f"/api/questions/{self.question.id}/vote/"

    def test_successful_vote(self):
        data = {"choice_id": self.choice1.id}
        response = self.client.post(self.vote_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Vote counted.")

        self.choice1.refresh_from_db()
        self.assertEqual(self.choice1.votes, 1)

    def test_invalid_choice_vote(self):
        data = {"choice_id": 9999}
        response = self.client.post(self.vote_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid choice ID.")

    def test_missing_choice_id(self):
        response = self.client.post(self.vote_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "choice_id is required.")
