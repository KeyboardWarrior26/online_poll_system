from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    expiry_date = models.DateTimeField('expiry date', null=True, blank=True)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_expired(self):
        return self.expiry_date and timezone.now() > self.expiry_date


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'choice')

    def __str__(self):
        return f"{self.user.username} voted for: {self.choice.choice_text} at {self.voted_at}"

