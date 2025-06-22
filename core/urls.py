# core/urls.py

from django.urls import path
from . import views # Import our custom views
# No longer import auth_views directly here, as auth URLs are handled by lms_project/urls.py

app_name = 'core' # Namespace for your app's URLs

urlpatterns = [
    path('', views.home, name='home'),

    # Removed: Custom Login/Logout URLs pointing to Django's built-in views.
    # These are now expected to be handled by the 'accounts/' include in lms_project/urls.py.
    # path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='core:home'), name='logout'),

    # Dashboard Redirection after successful login
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),

    # Role-based Dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('instructor-dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('sponsor-dashboard/', views.sponsor_dashboard, name='sponsor_dashboard'),

    # Course CRUD URLs
    path('courses/', views.course_list, name='course_list'), # List all courses
    path('courses/<int:pk>/', views.course_detail, name='course_detail'), # Course detail page
    path('courses/new/', views.course_create, name='course_create'), # Create new course
    path('courses/<int:pk>/edit/', views.course_update, name='course_update'), # Edit course
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'), # Delete course

    # Assessment URLs
    path('courses/<int:course_pk>/assessments/new/', views.assessment_create, name='assessment_create'), # Create assessment for a course

    # Submission & Grading URLs
    path('submissions/<int:pk>/grade/', views.submission_grade, name='submission_grade'), # Grade a submission
    path('submissions/<int:pk>/', views.submission_detail, name='submission_detail'), # Submission detail

    # Enrollment URL
    path('courses/<int:pk>/enroll/', views.enroll_course, name='enroll_course'),

    # Notification URLs
    path('notifications/', views.all_notifications, name='all_notifications'), # Page to view all notifications
    path('notifications/mark-read/<int:pk>/', views.mark_notification_as_read, name='mark_notification_as_read'), # API endpoint for AJAX
]
