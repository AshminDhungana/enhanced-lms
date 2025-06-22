# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from .models import (
    UserProfile, Course, Module, Lesson, Enrollment,
    Assessment, Submission, SponsorProfile, Sponsorship, CoursePayment,
    Notification # Import the new Notification model
)

# --- Custom Admin for UserProfile (to integrate with User model - unchanged) ---

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user profile'
    fields = ('role', 'bio', 'date_of_birth', 'phone_number')
    fk_name = 'user'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_profile_role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'profile__role')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'profile__role')

    def get_profile_role(self, obj):
        return obj.profile.get_role_display() if hasattr(obj, 'profile') else 'N/A'
    get_profile_role.short_description = 'Role'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# --- Registering Other Models (unchanged, just adding Notification) ---

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'price', 'is_active', 'created_at', 'updated_at')
    list_filter = ('difficulty', 'is_active')
    search_fields = ('title', 'description')
    filter_horizontal = ('instructors',)

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')
    list_filter = ('course',)
    search_fields = ('title', 'description', 'course__title')
    raw_id_fields = ('course',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'video_url', 'created_at')
    list_filter = ('module__course', 'module')
    search_fields = ('title', 'content', 'module__title')
    raw_id_fields = ('module',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'completion_date', 'is_completed', 'progress')
    list_filter = ('is_completed', 'course', 'student__profile__role')
    search_fields = ('student__username', 'course__title')
    raw_id_fields = ('student', 'course')

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'assessment_type', 'due_date', 'max_score')
    list_filter = ('assessment_type', 'course')
    search_fields = ('title', 'description', 'course__title')
    raw_id_fields = ('course',)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'student', 'submission_date', 'score', 'is_graded')
    list_filter = ('is_graded', 'assessment', 'student')
    search_fields = ('student__username', 'assessment__title', 'submission_content')
    raw_id_fields = ('assessment', 'student')

@admin.register(SponsorProfile)
class SponsorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization_name', 'contact_person', 'contact_email', 'total_funds_provided')
    search_fields = ('user__username', 'organization_name', 'contact_email')
    raw_id_fields = ('user',)

@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    list_display = ('sponsor', 'student', 'amount_funded', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'sponsor', 'student')
    search_fields = ('sponsor__username', 'student__username')
    raw_id_fields = ('sponsor', 'student')

@admin.register(CoursePayment)
class CoursePaymentAdmin(admin.ModelAdmin):
    list_display = ('course', 'payer', 'amount', 'payment_date', 'status', 'transaction_id')
    list_filter = ('status', 'payment_method', 'course')
    search_fields = ('transaction_id', 'payer__username', 'course__title')
    raw_id_fields = ('enrollment', 'payer', 'course')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Notification model.
    """
    list_display = ('recipient', 'notification_type', 'message', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at', 'recipient')
    search_fields = ('recipient__username', 'message', 'notification_type')
    raw_id_fields = ('recipient', 'sender') # Use raw ID fields for user foreign keys
    actions = ['mark_as_read', 'mark_as_unread'] # Custom actions for admins

    def mark_as_read(self, request, queryset):
        """Action to mark selected notifications as read."""
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} notification(s) marked as read.")
    mark_as_read.short_description = "Mark selected notifications as read"

    def mark_as_unread(self, request, queryset):
        """Action to mark selected notifications as unread."""
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} notification(s) marked as unread.")
    mark_as_unread.short_description = "Mark selected notifications as unread"