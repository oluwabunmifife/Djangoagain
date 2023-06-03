import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future = Question(pub_date=time)
        self.assertIs(future.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=days)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """Testing for no questions"""
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """Testing that past questions are displayed"""
        question = create_question(question_text="Past Question", days=-30)
        response = self.client.get(reverse("core:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question],)

    def test_future_question(self):
        """Testing that future questions aren't displayed"""    
        create_question(question_text="Future Question", days=30)
        response = self.client.get(reverse("core:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_and_past_question(self):
        """Testing that even if future and past questions are available, only the past ones are displayed"""
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("core:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question],)


    def two_past_questions(self):
        """Testing that two past questions are displayed"""
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("core:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question2, question1],)