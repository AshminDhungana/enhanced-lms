# lms_project/context_processors.py

from core.models import Notification

def notifications(request):
    """
    Context processor to add recent unread notifications and their count
    to the template context for authenticated users under a new key.
    """
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
        recent_notifications_list = list(unread_notifications[:5]) # Get up to 5 recent unread
        unread_count = unread_notifications.count()
        return {
            'global_notifications_data': { # Changed key from 'user' to 'global_notifications_data'
                'notifications': recent_notifications_list,
                'unread_count': unread_count,
            }
        }
    return {} # Return empty dict for unauthenticated users
