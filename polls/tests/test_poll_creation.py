from rest_framework.test import APITestCase
from django.urls import reverse
from polls.models import Question, Choice
from django.utils import timezone

class CreatePollTest(APITestCase):
    def test_create_poll_with_choices(self):
        url = reverse('question-list-create')
        data = {
            "question_text": "Best programming language?",
            "pub_date": timezone.now().isoformat(),
            "choices": [
                {"choice_text": "Python"},
                {"choice_text": "JavaScript"},
                {"choice_text": "Go"}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Choice.objects.count(), 3)
