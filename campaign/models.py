from django.db import models
from django.contrib.auth.models import User

class Campaign(models.Model):
    name = models.CharField(max_length=255)
    email_subject = models.CharField(max_length=255)
    email_body = models.TextField()
    recipients = models.TextField()
    scheduled_time = models.DateTimeField()
    sent = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ClickLog(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    recipient_email = models.EmailField()
    tracking_token = models.CharField(max_length=100, unique=True)
    clicked = models.BooleanField(default=False)
    click_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.recipient_email} - {self.campaign.name}"

class QuizQuestion(models.Model):
    question_text = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.campaign.name} - {self.score}"
