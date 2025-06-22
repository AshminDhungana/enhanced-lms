# lms_project/context_processors.py

from core.models import Notification

def notifications(request):
    """
    Context processor to add recent unread notifications and their count
    to the template context for authenticated users.
    """
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
        recent_notifications_list = list(unread_notifications[:5]) # Get up to 5 recent unread
        unread_count = unread_notifications.count()
        return {
            'user': { # Override the default 'user' object to include notification data
                'is_authenticated': request.user.is_authenticated,
                'username': request.user.username,
                # ... potentially other user fields you want to expose globally ...
                'recent_notifications': {
                    'notifications': recent_notifications_list,
                    'unread_count': unread_count,
                },
            }
        }
    return {} # Return empty dict for unauthenticated users