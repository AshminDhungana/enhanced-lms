# core/models.py

from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum, Avg, Max # Ensure Max is imported for sponsor dashboard


# --- User Profile and Roles (unchanged) ---

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
        ('sponsor', 'Sponsor'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student',
                            help_text="Defines the user's role within the LMS.")
    bio = models.TextField(blank=True, null=True,
                           help_text="A short biography or description for the user.")
    date_of_birth = models.DateField(blank=True, null=True,
                                     help_text="The user's date of birth.")
    phone_number = models.CharField(max_length=15, blank=True, null=True,
                                    help_text="The user's contact phone number.")

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        unique_together = ('user',)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    def clean(self):
        if self.role not in [choice[0] for choice in self.ROLE_CHOICES]:
            raise ValidationError(f"Invalid role: {self.role}")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.user.groups.clear()
        group, created = Group.objects.get_or_create(name=self.role)
        self.user.groups.add(group)

# --- Course Management (unchanged) ---

class Course(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    title = models.CharField(max_length=200, unique=True,
                             help_text="The title of the course.")
    description = models.TextField(
                                   help_text="A detailed description of the course content.")
    instructors = models.ManyToManyField(User, related_name='taught_courses',
                                         limit_choices_to={'groups__name': 'instructor'},
                                         help_text="Instructors who teach this course.")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner',
                                  help_text="The difficulty level of the course.")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                help_text="The price of the course.")
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text="Timestamp when the course was created.")
    updated_at = models.DateTimeField(auto_now=True,
                                      help_text="Timestamp of the last update to the course details.")
    is_active = models.BooleanField(default=True,
                                    help_text="Indicates if the course is currently active and available for enrollment.")

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['title']

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules',
                               help_text="The course to which this module belongs.")
    title = models.CharField(max_length=200,
                             help_text="The title of the module.")
    description = models.TextField(blank=True, null=True,
                                   help_text="A description of the module's content.")
    order = models.PositiveIntegerField(
                                        help_text="The order of the module within the course.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        ordering = ['course', 'order']
        unique_together = ('course', 'order')

    def __str__(self):
        return f"{self.course.title} - Module {self.order}: {self.title}"

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons',
                               help_text="The module to which this lesson belongs.")
    title = models.CharField(max_length=200,
                             help_text="The title of the lesson.")
    content = models.TextField(
                              help_text="The main content of the lesson (e.g., text, HTML, markdown).")
    video_url = models.URLField(blank=True, null=True,
                                help_text="Optional URL for a video associated with the lesson.")
    order = models.PositiveIntegerField(
                                        help_text="The order of the lesson within the module.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        ordering = ['module', 'order']
        unique_together = ('module', 'order')

    def __str__(self):
        return f"{self.module.course.title} - {self.module.title} - Lesson {self.order}: {self.title}"

# --- Enrollment and Progress (unchanged) ---

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments',
                                limit_choices_to={'groups__name': 'student'},
                                help_text="The student enrolled in the course.")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments',
                               help_text="The course the student is enrolled in.")
    enrollment_date = models.DateTimeField(auto_now_add=True,
                                           help_text="The date and time of enrollment.")
    completion_date = models.DateTimeField(blank=True, null=True,
                                           help_text="The date and time when the student completed the course.")
    is_completed = models.BooleanField(default=False,
                                       help_text="Indicates if the student has completed the course.")
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00,
                                   help_text="The student's progress in the course as a percentage (0.00 to 100.00).")

    class Meta:
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        unique_together = ('student', 'course')
        ordering = ['-enrollment_date']

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"

# --- Assessments (unchanged) ---

class Assessment(models.Model):
    ASSESSMENT_TYPES = [
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('exam', 'Exam'),
        ('project', 'Project'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assessments',
                               help_text="The course this assessment belongs to.")
    title = models.CharField(max_length=200,
                             help_text="The title of the assessment.")
    description = models.TextField(blank=True, null=True,
                                   help_text="A description of the assessment requirements.")
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPES, default='quiz',
                                       help_text="The type of assessment.")
    due_date = models.DateTimeField(
                                    help_text="The deadline for completing this assessment.")
    max_score = models.PositiveIntegerField(
                                            help_text="The maximum possible score for this assessment.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Assessment"
        verbose_name_plural = "Assessments"
        ordering = ['-due_date', 'course__title', 'title']

    def __str__(self):
        return f"{self.title} for {self.course.title}"

class Submission(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='submissions',
                                   help_text="The assessment to which this submission belongs.")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions',
                                limit_choices_to={'groups__name': 'student'},
                                help_text="The student who submitted this assessment.")
    submission_date = models.DateTimeField(auto_now_add=True,
                                            help_text="The date and time of the submission.")
    submission_content = models.TextField(blank=True, null=True,
                                          help_text="The content of the submission (e.g., text, answers, link to file).")
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                help_text="The score received for this submission.")
    feedback = models.TextField(blank=True, null=True,
                                help_text="Feedback provided by the instructor on the submission.")
    is_graded = models.BooleanField(default=False,
                                    help_text="Indicates if the submission has been graded.")

    class Meta:
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"
        unique_together = ('assessment', 'student')
        ordering = ['-submission_date']

    def __str__(self):
        return f"Submission by {self.student.username} for {self.assessment.title}"

# --- Sponsorship (unchanged) ---

class SponsorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sponsor_profile',
                                limit_choices_to={'groups__name': 'sponsor'},
                                help_text="The associated user with 'sponsor' role.")
    organization_name = models.CharField(max_length=255, blank=True, null=True,
                                         help_text="Name of the organization the sponsor represents.")
    contact_person = models.CharField(max_length=100, blank=True, null=True,
                                      help_text="Name of the primary contact person at the organization.")
    contact_email = models.EmailField(blank=True, null=True,
                                      help_text="Email for the sponsor's contact person.")
    total_funds_provided = models.DecimalField(max_digits=12, decimal_places=2, default=0.00,
                                               help_text="Total funds provided by this sponsor.")

    class Meta:
        verbose_name = "Sponsor Profile"
        verbose_name_plural = "Sponsor Profiles"

    def __str__(self):
        return f"Sponsor: {self.organization_name or self.user.username}"

class Sponsorship(models.Model):
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sponsored_students',
                                limit_choices_to={'groups__name': 'sponsor'},
                                help_text="The sponsor providing the funding.")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_sponsorships',
                                limit_choices_to={'groups__name': 'student'},
                                help_text="The student receiving the sponsorship.")
    amount_funded = models.DecimalField(max_digits=10, decimal_places=2,
                                        help_text="The amount of money provided by the sponsor for this sponsorship.")
    start_date = models.DateField(default=timezone.now,
                                  help_text="The date when the sponsorship began.")
    end_date = models.DateField(blank=True, null=True,
                                help_text="The date when the sponsorship is expected to end.")
    is_active = models.BooleanField(default=True,
                                    help_text="Indicates if the sponsorship is currently active.")
    notes = models.TextField(blank=True, null=True,
                             help_text="Any additional notes about the sponsorship.")

    class Meta:
        verbose_name = "Sponsorship"
        verbose_name_plural = "Sponsorships"
        unique_together = ('sponsor', 'student', 'start_date')
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.sponsor.username} sponsoring {self.student.username} for ${self.amount_funded}"

# --- Optional: Course Payments (unchanged) ---

class CoursePayment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='payment',
                                      blank=True, null=True,
                                      help_text="The enrollment associated with this payment.")
    payer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='payments_made',
                              help_text="The user who made the payment (can be student or sponsor).")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments',
                               help_text="The course for which the payment was made.")
    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                 help_text="The amount paid for the course.")
    payment_date = models.DateTimeField(auto_now_add=True,
                                        help_text="The date and time the payment was made.")
    transaction_id = models.CharField(max_length=255, unique=True, blank=True, null=True,
                                      help_text="Unique transaction ID from the payment gateway.")
    payment_method = models.CharField(max_length=50, blank=True, null=True,
                                      help_text="Method of payment (e.g., 'Stripe', 'PayPal', 'Card').")
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending',
                              help_text="Status of the payment.")

    class Meta:
        verbose_name = "Course Payment"
        verbose_name_plural = "Course Payments"
        ordering = ['-payment_date']

    def __str__(self):
        return f"Payment of ${self.amount} for {self.course.title} by {self.payer.username} - {self.get_status_display()}"


# --- New: Notification Model ---

class Notification(models.Model):
    """
    Model to store in-app notifications for users.
    """
    NOTIFICATION_TYPES = [
        ('course_deadline', 'Course Deadline'),
        ('assessment_result', 'Assessment Result'),
        ('new_assignment', 'New Assignment'),
        ('progress_report', 'Progress Report'),
        ('engagement_alert', 'Engagement Alert'),
        ('general', 'General Announcement'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications',
                                  help_text="The user who will receive this notification.")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='sent_notifications',
                               help_text="The user who triggered this notification (e.g., instructor, admin).")
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES,
                                         help_text="The type of notification (e.g., deadline, result, new assignment).")
    message = models.TextField(help_text="The content of the notification message.")
    link = models.URLField(max_length=500, blank=True, null=True,
                           help_text="Optional URL for the user to click to view more details.")
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text="Timestamp when the notification was created.")
    is_read = models.BooleanField(default=False,
                                  help_text="Indicates if the recipient has read the notification.")

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-created_at'] # Order by most recent first

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.get_notification_type_display()} - {self.message[:50]}..."