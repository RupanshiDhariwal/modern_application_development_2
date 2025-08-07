from app import celery_app
from celeryContext import ContextTask
from mailer import mail
from models import User, Ad_request 


@celery_app.task(base=ContextTask)
def sum():
    print("Sum function called")
    import time
    time.sleep(10)
    return 1+2


@celery_app.task(base=ContextTask)
def test_db():
    from models import Category
    var1 = Category.query.first()
    print(var1.name)
    return "DB test done"

from datetime import datetime, timedelta
from sqlalchemy import or_ , and_

# Function to check if an influencer has pending ad requests and has not logged in recently
def has_pending_ad_requests(user_id, last_login_threshold):
    # Check if there are any pending ad requests assigned to the user or public ad requests
    has_pending_requests = Ad_request.query.filter(
        or_(
            and_(Ad_request.user_id == user_id, Ad_request.status == 'pending'),
            and_(Ad_request.status == 'public')  # Assuming 'public' status indicates a public ad request
        )
    ).count() > 0
    
    # Check if the user has logged in since the last login threshold
    user = User.query.get(user_id)
    if user:
        last_login = user.last_login  # Assuming 'last_login' is a field in your User model
        if last_login is None or last_login < last_login_threshold:
            return has_pending_requests
    
    return False

# Celery task to send reminder emails
@celery_app.task(base=ContextTask)
def test_mail(base=ContextTask):
    from flask_mail import Message
    from models import User
    from app import app  # Assuming you have an app instance where mail is initialized

    
    email_sub = "Reminder: Check Your Ad Requests"
    
    # Define the threshold for the last login (e.g., 30 days ago)
    last_login_threshold = datetime.utcnow() - timedelta(days=1)
    
    # Query users who are influencers (role ID 3) or have the role 'influencer'
    users = User.query.filter(
        (User.role_id == 3) | (User.role == 'influencer')
    ).all()
    
    for user in users:
        if has_pending_ad_requests(user.id, last_login_threshold):
            html_body = "<html><body>"
            html_body += f"<h1>Hi {user.name},</h1>"  # Assuming 'name' is a field in your User model
            html_body += "<p>You have pending ad requests that need your attention.</p>"
            html_body += "<p>Please visit your ad requests or check out the public ad requests.</p>"
            html_body += "</body></html>"

            msg = Message(subject=email_sub, recipients=[user.email])
            msg.html = html_body
            mail.send(msg)
    
    return "Reminder emails sent"




from flask import render_template
from models import Campaign, Ad_request, Sponsor
from datetime import datetime, timedelta

def generate_monthly_report(sponsor_id):
    # Get the start and end date of the current month
    now = datetime.utcnow()
    start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_date = (start_date + timedelta(days=31)).replace(day=1)  # First day of next month

    # Fetch data specific to the sponsor
    campaigns = Campaign.query.filter(
        Campaign.created_by == sponsor_id,
        Campaign.created_at >= start_date,
        Campaign.created_at < end_date
    ).all()
    ad_requests = Ad_request.query.filter(
        Ad_request.created_by == sponsor_id,
        Ad_request.created_at >= start_date,
        Ad_request.created_at < end_date
    ).all()

    # Aggregate data
    report_data = {
        'campaigns': campaigns,
        'advertisements': ad_requests,
        'growth_in_sales': sum(ad.campaign.sales_growth for ad in ad_requests if ad.campaign),
        'budget_used': sum(ad.campaign.budget_used for ad in ad_requests if ad.campaign),
        'budget_remaining': sum(ad.campaign.budget_remaining for ad in ad_requests if ad.campaign),
    }
    
    # Render the HTML report using a template
    html_report = render_template('monthly_report.html', data=report_data)
    return html_report



@celery_app.task(base=ContextTask)
def send_monthly_report(base=ContextTask):
    from flask_mail import Message
    from models import Sponsor
    email_sub = "Monthly Activity Report"
    
    # Get all sponsors
    sponsors = Sponsor.query.all()
    
    for sponsor in sponsors:
        # Generate the report for the specific sponsor
        html_report = generate_monthly_report(sponsor.id)
        
        # Send the email
        msg = Message(subject=email_sub, recipients=[sponsor.email])
        msg.html = html_report
        mail.send(msg)
    
    return "Monthly reports sent"



import csv
import io
from models import Campaign

def generate_campaign_csv(sponsor_id):
    # Fetch campaigns for the specific sponsor
    campaigns = Campaign.query.filter_by(created_by=sponsor_id).all()

    # Create an in-memory file-like object
    output = io.StringIO()
    writer = csv.writer(output)

    # Write the header
    writer.writerow(['Campaign ID', 'Description', 'Start Date', 'End Date', 'Budget', 'Visibility', 'Goals'])

    # Write campaign data
    for campaign in campaigns:
        writer.writerow([
            campaign.id,
            campaign.description,
            campaign.start_date,
            campaign.end_date,
            campaign.budget,
            campaign.visibility,
            campaign.goals
        ])

    # Get the CSV content
    csv_content = output.getvalue()
    output.close()

    return csv_content



@celery_app.task(base=ContextTask)
def export_campaign_csv(sponsor_id, user_email):
    from flask_mail import Message
    from models import Sponsor
    csv_content = generate_campaign_csv(sponsor_id)

    # Save CSV to a file or an appropriate storage (optional)
    # with open('campaign_export.csv', 'w') as f:
    #     f.write(csv_content)

    msg = Message(subject="Your Campaign Export is Ready", recipients=[user_email])
    msg.body = "Your campaign export is complete. Please find the CSV file attached."
    msg.attach("campaign_export.csv", "text/csv", csv_content)
    mail.send(msg)

    return "Export completed and email sent"



