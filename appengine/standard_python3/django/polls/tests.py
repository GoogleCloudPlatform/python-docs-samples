from django.test import Client, TestCase  # noqa: 401
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question


class PollViewTests(TestCase):
    def setUp(self):
        question = Question(
            question_text="This is a test question",
            pub_date=timezone.now()
        )
        question.save()
        self.question = question

        choice = Choice(
            choice_text="This is a test choice",
            votes=0
        )
        choice.question = question
        choice.save()
        self.choice = choice

        self.client = Client()

    def test_index_view(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert self.question.question_text in str(response.content)

    def test_detail_view(self):
        response = self.client.get(
            reverse('polls:detail', args=(self.question.id,)))
        assert response.status_code == 200
        assert self.question.question_text in str(response.content)
        assert self.choice.choice_text in str(response.content)

    def test_results_view(self):
        response = self.client.get(
            reverse('polls:results', args=(self.question.id,)))
        assert response.status_code == 200
        assert self.question.question_text in str(response.content)
        assert self.choice.choice_text in str(response.content)
