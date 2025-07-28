from django.test import TestCase
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from polls.models import Question, Choice, Vote

class VoteTrendsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.now = timezone.now()

        # Create a sample question and choice
        self.question = Question.objects.create(
            question_text="Trend question",
            pub_date=self.now
        )
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text="Choice A"
        )

        # Create votes on different days using different users
        for i in range(5):
            user = User.objects.create_user(username=f'user{i}', password='pass')
            Vote.objects.create(
                user=user,
                choice=self.choice,
                voted_at=self.now - timedelta(days=i)
            )

        # Login with a test user to perform API requests
        self.test_user = User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')

    def test_vote_trends_by_day(self):
        url = f'/api/vote-trends/?question_id={self.question.id}&interval=day'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('labels', response.data)
        self.assertIn('data', response.data)
        self.assertTrue(len(response.data['labels']) > 0)

    def test_vote_trends_by_week(self):
        url = f'/api/vote-trends/?question_id={self.question.id}&interval=week'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('labels', response.data)
        self.assertIn('data', response.data)
        self.assertTrue(len(response.data['labels']) > 0)

    def test_vote_trends_invalid_interval(self):
        url = f'/api/vote-trends/?question_id={self.question.id}&interval=invalid'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)

