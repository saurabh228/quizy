from django.db import models
from django.conf import settings

import uuid

class Question(models.Model):
    """
    Model representing a quiz question.
    """
    QUESTION_TYPE_CHOICES = [
        ('single', 'Single Correct'),
        ('multiple', 'Multiple Correct'),
    ]

    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_options = models.JSONField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES, default='single')

    def __str__(self):
        return f"Question {self.id}: {self.question_text[:50]}..."

class QuizSession(models.Model):
    """
    Model representing a user's quiz session.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_questions = models.IntegerField(default=10)
    completed_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    incorrect_answers = models.IntegerField(default=0)
    partially_correct_answers = models.IntegerField(default=0)
    score = models.FloatField(default=0.0)
    is_completed = models.BooleanField(default=False)
    current_question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.SET_NULL)

    # Timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    session_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Session {self.id} - {self.user.username}"

class SessionQuestion(models.Model):
    """
    Model representing a question within a quiz session, storing user's selected options.
    """
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name='session_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_options = models.JSONField()
    score = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('session', 'question')

    def __str__(self):
        return f"Session {self.session.id} - Question {self.question.id}"