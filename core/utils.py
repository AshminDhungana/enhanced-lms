# core/utils.py

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from .models import Notification # Import your Notification model

def send_notification_email(recipient_user, subject, template_name, context, notification_type, sender_user=None, link=None):
    """
    Sends an email and creates an in-app notification record.

    Args:
        recipient_user (User): The Django User object who will receive the email and notification.
        subject (str): The subject line of the email.
        template_name (str): The name of the HTML email template (e.g., 'emails/new_assignment.html').
                             This template should reside in your 'templates' directory.
        context (dict): A dictionary of data to pass to the email template.
        notification_type (str): The type of notification (e.g., 'new_assignment', 'progress_report').
                                 Must match one of the choices in Notification.NOTIFICATION_TYPES.
        sender_user (User, optional): The Django User object who triggered the notification. Defaults to None.
        link (str, optional): An optional URL related to the notification. Defaults to None.
    """
    # 1. Render the HTML email content from a template
    html_message = render_to_string(template_name, context)

    # 2. Create a plain text version of the email for clients that don't support HTML
    plain_message = strip_tags(html_message)

    # 3. Send the email
    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL, # From email defined in settings.py
            [recipient_user.email],
            html_message=html_message,
            fail_silently=False, # Raise exception if email fails
        )
        print(f"Email sent successfully to {recipient_user.email} for '{subject}'")
    except Exception as e:
        print(f"Failed to send email to {recipient_user.email}: {e}")
        # Log the error for production environments

    # 4. Create an in-app notification record
    try:
        Notification.objects.create(
            recipient=recipient_user,
            sender=sender_user,
            notification_type=notification_type,
            message=subject, # Use subject as a concise message for in-app display
            link=link,
            is_read=False # New notifications are unread by default
        )
        print(f"In-app notification created for {recipient_user.username}: '{subject}'")
    except Exception as e:
        print(f"Failed to create in-app notification for {recipient_user.username}: {e}")
        # Log the error