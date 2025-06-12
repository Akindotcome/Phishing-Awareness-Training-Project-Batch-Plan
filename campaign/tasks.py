from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Campaign, ClickLog
import uuid

@shared_task
def send_campaign_emails():
    from django.conf import settings
    campaigns = Campaign.objects.filter(sent=False, scheduled_time__lte=timezone.now())
    for campaign in campaigns:
        recipients = [email.strip() for email in campaign.recipients.split(',') if email.strip()]
        for recipient in recipients:
            unique_token = uuid.uuid4().hex
            track_link = f"http://localhost:8000/track/{campaign.id}/{unique_token}/"

            ClickLog.objects.create(
                campaign=campaign,
                recipient_email=recipient,
                tracking_token=unique_token
            )

            send_mail(
                campaign.email_subject,
                f"{campaign.email_body}

Click here: {track_link}",
                settings.EMAIL_HOST_USER,
                [recipient],
                fail_silently=False,
            )
        campaign.sent = True
        campaign.save()
