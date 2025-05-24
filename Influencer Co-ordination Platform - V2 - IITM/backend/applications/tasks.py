from .workers import celery 
from celery.schedules import crontab
from .models import Influencer
from .email_config import send_email



@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_tasks(
        # crontab(minute=0, hour=16),
        crontab(),
        daily_reminder.s(),
        name = "daily reminder"
        
    )

    sender.add_periodic_tasks(
        crontab(0,0,day_of_month=1),
        monthly_report.s(),
        name = "monthy report"
        
    )


@celery.task()
def daily_reminder():
    influencers = Influencer.query.all()
    for influencer in influencers:
        message = "this is the daily reminder template"
        send_email(to=influencer.influencer_email, sub="Your daily reminder", message=message)
        print("DAILY_REMINDER")
        return ("DAILY REMINDER")
    

@celery.task()
def monthly_report():
    influencers = Influencer.query.all()
    for influencer in influencers:
        message = "this is the monthly report template"
        send_email(to=influencer.influencer_email, sub="Your monthly report", message=message)
        print("monthly_report")
        return ("monthly_report")





