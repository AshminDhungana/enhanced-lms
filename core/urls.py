# core/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),

    # Auth URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:home'), name='logout'),

    # Dashboard Redirection
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),

    # Role-based Dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('instructor-dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('sponsor-dashboard/', views.sponsor_dashboard, name='sponsor_dashboard'),

    # Course CRUD URLs
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/new/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),

    # Assessment URLs
    path('courses/<int:course_pk>/assessments/new/', views.assessment_create, name='assessment_create'), # New: Create assessment for a course

    # Submission & Grading URLs
    path('submissions/<int:pk>/grade/', views.submission_grade, name='submission_grade'), # New: Grade a submission
    path('submissions/<int:pk>/', views.submission_detail, name='submission_detail'), # New: Submission detail

    # Enrollment URL
    path('courses/<int:pk>/enroll/', views.enroll_course, name='enroll_course'),

    # Notification URLs
    path('notifications/', views.all_notifications, name='all_notifications'),
    path('notifications/mark-read/<int:pk>/', views.mark_notification_as_read, name='mark_notification_as_read'),
]