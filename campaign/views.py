from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Campaign, ClickLog, QuizQuestion, QuizResult
from .forms import QuizForm

def track_click(request, campaign_id, tracking_token):
    try:
        log = ClickLog.objects.get(campaign_id=campaign_id, tracking_token=tracking_token)
        log.clicked = True
        log.click_time = timezone.now()
        log.save()
    except ClickLog.DoesNotExist:
        return HttpResponse("Invalid tracking link.", status=404)

    return redirect('phishing_quiz', campaign_id=campaign_id)

@login_required
def phishing_quiz(request, campaign_id):
    questions = QuizQuestion.objects.all()[:5]
    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            for question in questions:
                user_answer = form.cleaned_data.get(f'question_{question.id}')
                if user_answer == question.correct_answer:
                    score += 1
            QuizResult.objects.create(
                user=request.user,
                campaign_id=campaign_id,
                score=score
            )
            return render(request, 'campaign/quiz_result.html', {'score': score, 'total': len(questions)})
    else:
        form = QuizForm(questions=questions)

    return render(request, 'campaign/quiz.html', {'form': form})

@login_required
def reporting_dashboard(request):
    if request.user.role != 'Admin':
        return redirect('dashboard')

    campaigns = Campaign.objects.filter(created_by=request.user)
    report_data = []

    for campaign in campaigns:
        total_recipients = len([email.strip() for email in campaign.recipients.split(',') if email.strip()])
        clicks = ClickLog.objects.filter(campaign=campaign, clicked=True).count()
        click_rate = (clicks / total_recipients) * 100 if total_recipients else 0

        quiz_participants = QuizResult.objects.filter(campaign=campaign).count()
        avg_score = QuizResult.objects.filter(campaign=campaign).aggregate(models.Avg('score'))['score__avg'] or 0

        report_data.append({
            'campaign': campaign,
            'click_rate': round(click_rate, 2),
            'quiz_participants': quiz_participants,
            'avg_score': round(avg_score, 2),
        })

    return render(request, 'campaign/reporting_dashboard.html', {'report_data': report_data})
