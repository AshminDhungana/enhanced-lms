# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.urls import reverse
from .models import Course, Enrollment, Assessment, Submission, Sponsorship, UserProfile, CoursePayment, Notification
from django.db.models import Count, Q, Sum, Avg, Max
from django.utils import timezone
from .forms import CourseForm, EnrollmentForm, AssessmentForm, SubmissionGradingForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import send_notification_email
from django.http import JsonResponse


# --- Helper functions for checking user roles ---
def is_admin(user):
    return user.is_authenticated and user.groups.filter(name='admin').exists()

def is_instructor(user):
    return user.is_authenticated and user.groups.filter(name='instructor').exists()

def is_student(user):
    return user.is_authenticated and user.groups.filter(name='student').exists()

def is_sponsor(user):
    return user.is_authenticated and user.groups.filter(name='sponsor').exists()


# --- Home Page View ---
def home(request):
    return render(request, 'core/home.html')

# --- Dashboard Redirection View ---
@login_required
def dashboard_redirect(request):
    if is_admin(request.user) or request.user.is_superuser:
        return redirect('core:admin_dashboard')
    elif is_student(request.user):
        return redirect('core:student_dashboard')
    elif is_instructor(request.user):
        return redirect('core:instructor_dashboard')
    elif is_sponsor(request.user):
        return redirect('core:sponsor_dashboard')
    else:
        return redirect('core:home')


# --- Role-based Dashboards ---

@login_required
@user_passes_test(is_student, login_url='/login/')
def student_dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    upcoming_assignments = Assessment.objects.filter(
        course__in=[e.course for e in enrollments],
        due_date__gte=timezone.now()
    ).order_by('due_date')[:5]

    context = {
        'user': request.user,
        'enrollments': enrollments,
        'upcoming_assignments': upcoming_assignments,
    }
    return render(request, 'core/dashboard_student.html', context)

@login_required
@user_passes_test(is_instructor, login_url='/login/')
def instructor_dashboard(request):
    taught_courses = Course.objects.filter(instructors=request.user).annotate(
        total_students=Count('enrollments')
    )
    pending_submissions = Submission.objects.filter(
        assessment__course__in=taught_courses,
        is_graded=False
    ).order_by('assessment__due_date')[:5]

    total_active_courses = taught_courses.filter(is_active=True).count()
    total_students_across_courses = Enrollment.objects.filter(course__in=taught_courses).distinct('student').count()

    context = {
        'user': request.user,
        'taught_courses': taught_courses,
        'pending_submissions': pending_submissions,
        'total_active_courses': total_active_courses,
        'total_students_across_courses': total_students_across_courses,
    }
    return render(request, 'core/dashboard_instructor.html', context)

@login_required
@user_passes_test(is_sponsor, login_url='/login/')
def sponsor_dashboard(request):
    current_sponsor_user = request.user
    all_sponsorships = Sponsorship.objects.filter(sponsor=current_sponsor_user).select_related('student')

    student_status_filter = request.GET.get('status', 'all')
    student_progress_filter = request.GET.get('progress', 'all')

    filtered_sponsored_student_data = []
    total_completed_by_sponsored = 0
    total_in_progress_by_sponsored = 0
    total_sponsored_enrollments = 0
    sum_progress_for_avg = 0
    count_progress_for_avg = 0

    for sponsorship in all_sponsorships:
        student = sponsorship.student
        student_enrollments = Enrollment.objects.filter(student=student)

        has_completed_courses = student_enrollments.filter(is_completed=True).exists()
        has_in_progress_courses = student_enrollments.filter(is_completed=False).exists()

        overall_progress_value = 0
        if student_enrollments.exists():
            for enrollment in student_enrollments:
                if enrollment.progress is not None:
                    sum_progress_for_avg += enrollment.progress
                    count_progress_for_avg += 1

            max_progress = student_enrollments.aggregate(Max('progress'))['progress__max']
            overall_progress_value = max_progress if max_progress is not None else 0

        if has_completed_courses:
            total_completed_by_sponsored += 1
        if has_in_progress_courses:
            total_in_progress_by_sponsored += 1
        total_sponsored_enrollments += student_enrollments.count()

        if student_status_filter == 'completed' and not has_completed_courses:
            continue
        if student_progress_filter == 'high_progress' and overall_progress_value < 75:
            continue
        if student_progress_filter == 'low_progress' and overall_progress_value >= 25:
            continue

        filtered_sponsored_student_data.append({
            'student': student,
            'sponsorship': sponsorship,
            'enrollments': student_enrollments,
            'has_completed_courses': has_completed_courses,
            'has_in_progress_courses': has_in_progress_courses,
            'overall_progress_value': overall_progress_value,
        })

    avg_sponsored_student_progress = (sum_progress_for_avg / count_progress_for_avg) if count_progress_for_avg > 0 else 0

    total_students_sponsored = all_sponsorships.count()
    total_active_sponsorships = all_sponsorships.filter(is_active=True).count()
    total_funds_provided = all_sponsorships.aggregate(total_sum=Sum('amount_funded'))['total_sum']
    if total_funds_provided is None:
        total_funds_provided = 0

    total_funds_utilized = CoursePayment.objects.filter(
        payer=current_sponsor_user,
        status='completed'
    ).aggregate(sum_paid=Sum('amount'))['sum_paid']
    if total_funds_utilized is None:
        total_funds_utilized = 0

    paginator = Paginator(filtered_sponsored_student_data, 10)
    page = request.GET.get('page')
    try:
        sponsored_students_page = paginator.page(page)
    except PageNotAnInteger:
        sponsored_students_page = paginator.page(1)
    except EmptyPage:
        sponsored_students_page = paginator.page(paginator.num_pages)

    context = {
        'user': request.user,
        'sponsorships': all_sponsorships,
        'filtered_sponsored_student_data': sponsored_students_page,
        'total_students_sponsored': total_students_sponsored,
        'total_active_sponsorships': total_active_sponsorships,
        'total_funds_provided': total_funds_provided,
        'total_funds_utilized': total_funds_utilized,
        'student_status_filter': student_status_filter,
        'student_progress_filter': student_progress_filter,
        'total_completed_by_sponsored': total_completed_by_sponsored,
        'total_in_progress_by_sponsored': total_in_progress_by_sponsored,
        'total_sponsored_enrollments': total_sponsored_enrollments,
        'avg_sponsored_student_progress': avg_sponsored_student_progress,
    }
    return render(request, 'core/dashboard_sponsor.html', context)


# --- Admin Dashboard Analytics ---
@login_required
@user_passes_test(lambda u: is_admin(u) or u.is_superuser, login_url='/login/')
def admin_dashboard(request):
    total_users = User.objects.count()
    total_students = UserProfile.objects.filter(role='student').count()
    total_instructors = UserProfile.objects.filter(role='instructor').count()
    total_sponsors = UserProfile.objects.filter(role='sponsor').count()
    total_admins = UserProfile.objects.filter(role='admin').count()

    total_courses = Course.objects.count()
    active_courses = Course.objects.filter(is_active=True).count()

    total_enrollments = Enrollment.objects.count()
    completed_enrollments = Enrollment.objects.filter(is_completed=True).count()
    average_completion_rate = Enrollment.objects.aggregate(avg_progress=Avg('progress'))['avg_progress']
    if average_completion_rate is None:
        average_completion_rate = 0

    total_sponsorships = Sponsorship.objects.count()
    total_funds_received = Sponsorship.objects.aggregate(sum_amount=Sum('amount_funded'))['sum_amount']
    if total_funds_received is None:
        total_funds_received = 0
    
    context = {
        'user': request.user,
        'total_users': total_users,
        'total_students': total_students,
        'total_instructors': total_instructors,
        'total_sponsors': total_sponsors,
        'total_admins': total_admins,
        'total_courses': total_courses,
        'active_courses': active_courses,
        'total_enrollments': total_enrollments,
        'completed_enrollments': completed_enrollments,
        'average_completion_rate': average_completion_rate,
        'total_sponsorships': total_sponsorships,
        'total_funds_received': total_funds_received,
    }
    return render(request, 'core/dashboard_admin.html', context)


# --- Course CRUD Views ---

def course_list(request):
    courses = Course.objects.filter(is_active=True)
    search_query = request.GET.get('q')
    difficulty_filter = request.GET.get('difficulty')
    instructor_filter = request.GET.get('instructor')

    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(instructors__first_name__icontains=search_query) |
            Q(instructors__last_name__icontains=search_query)
        ).distinct()

    if difficulty_filter and difficulty_filter != 'all':
        courses = courses.filter(difficulty=difficulty_filter)

    if instructor_filter:
        courses = courses.filter(
            Q(instructors__username__icontains=instructor_filter) |
            Q(instructors__first_name__icontains=instructor_filter) |
            Q(instructors__last_name__icontains=instructor_filter)
        ).distinct()

    courses = courses.order_by('title')

    paginator = Paginator(courses, 9)
    page = request.GET.get('page')

    try:
        courses_page = paginator.page(page)
    except PageNotAnInteger:
        courses_page = paginator.page(1)
    except EmptyPage:
        courses_page = paginator.page(paginator.num_pages)

    context = {
        'courses': courses_page,
        'search_query': search_query,
        'difficulty_filter': difficulty_filter,
        'instructor_filter': instructor_filter,
        'difficulty_choices': Course.DIFFICULTY_CHOICES
    }
    return render(request, 'core/course_list.html', context)


@login_required
@user_passes_test(is_instructor, login_url='/login/')
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            form.save_m2m()
            course.instructors.add(request.user)
            return redirect('core:course_list')
    else:
        form = CourseForm()
    context = {'form': form, 'form_title': 'Create New Course'}
    return render(request, 'core/course_form.html', context)

@login_required
@user_passes_test(is_instructor, login_url='/login/')
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    # Authorization check
    if not course.instructors.filter(pk=request.user.pk).exists() and not request.user.is_superuser:
        return redirect('core:course_list')

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            # Redirect to course detail after update for better UX
            return redirect('core:course_detail', pk=course.pk) 
    else:
        form = CourseForm(instance=course)
    
    # These lines should be at the same indentation level as the 'if request.method == 'POST':'
    # and the 'else:'. This was likely the source of the SyntaxError.
    context = {'form': form, 'form_title': 'Update Course', 'course': course}
    return render(request, 'core/course_form.html', context)

@login_required
@user_passes_test(is_instructor, login_url='/login/')
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if not course.instructors.filter(pk=request.user.pk).exists() and not request.user.is_superuser:
        return redirect('core:course_list')

    if request.method == 'POST':
        course.delete()
        return redirect('core:course_list')
    context = {'course': course}
    return render(request, 'core/course_confirm_delete.html', context)

def course_detail(request, pk):
    course = get_object_or_404(Course.objects.prefetch_related('modules__lessons'), pk=pk)
    is_enrolled = False
    if request.user.is_authenticated:
        if request.user.is_superuser or is_admin(request.user) or is_instructor(request.user):
            is_enrolled = True
        else:
            is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()

    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'user': request.user,
    }
    return render(request, 'core/course_detail.html', context)

@login_required
@user_passes_test(is_student, login_url='/login/')
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        return redirect('core:course_detail', pk=course.pk)

    if request.method == 'POST':
        enrollment = Enrollment.objects.create(student=request.user, course=course)
        return redirect('core:student_dashboard')
    return redirect('core:course_detail', pk=course.pk)


# --- New Views for Assessment and Submission Grading with Notifications ---

@login_required
@user_passes_test(is_instructor, login_url='/login/')
def assessment_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if not course.instructors.filter(pk=request.user.pk).exists() and not request.user.is_superuser:
        return redirect('core:course_detail', pk=course.pk)

    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.course = course
            assessment.save()

            enrolled_students = User.objects.filter(enrollments__course=course)
            # Use build_absolute_uri to ensure the link is fully qualified for emails
            assignment_link = request.build_absolute_uri(reverse('core:course_detail', args=[course.pk])) 

            for student in enrolled_students:
                context = {
                    'student_name': student.first_name or student.username,
                    'course_title': course.title,
                    'assignment_title': assessment.title,
                    'due_date': assessment.due_date,
                    'assignment_link': assignment_link,
                }
                send_notification_email(
                    recipient_user=student,
                    subject=f"New Assignment: {assessment.title} for {course.title}",
                    template_name='emails/new_assignment.html',
                    context=context,
                    notification_type='new_assignment',
                    sender_user=request.user,
                    link=assignment_link
                )

            return redirect('core:course_detail', pk=course.pk)
    else:
        form = AssessmentForm(initial={'course': course})
    
    context = {'form': form, 'form_title': f'Create New Assignment for {course.title}', 'course': course}
    return render(request, 'core/assessment_form.html', context)


@login_required
@user_passes_test(is_instructor, login_url='/login/')
def submission_grade(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    assessment = submission.assessment
    course = assessment.course

    if not course.instructors.filter(pk=request.user.pk).exists() and not request.user.is_superuser:
        return redirect('core:instructor_dashboard')

    if request.method == 'POST':
        form = SubmissionGradingForm(request.POST, instance=submission, assessment_max_score=assessment.max_score)
        if form.is_valid():
            graded_submission = form.save()

            submission_link = request.build_absolute_uri(reverse('core:submission_detail', args=[graded_submission.pk]))

            context = {
                'student_name': graded_submission.student.first_name or graded_submission.student.username,
                'assignment_title': assessment.title,
                'course_title': course.title,
                'score': graded_submission.score,
                'max_score': assessment.max_score,
                'feedback': graded_submission.feedback,
                'submission_link': submission_link,
            }
            send_notification_email(
                recipient_user=graded_submission.student,
                subject=f"Assessment Graded: {assessment.title} - {graded_submission.score}/{assessment.max_score}",
                template_name='emails/assessment_graded.html',
                context=context,
                notification_type='assessment_result',
                sender_user=request.user,
                link=submission_link
            )

            return redirect('core:instructor_dashboard')
    else:
        form = SubmissionGradingForm(instance=submission, assessment_max_score=assessment.max_score)
    
    context = {
        'form': form,
        'form_title': f'Grade Submission for {submission.student.username}',
        'submission': submission,
        'assessment': assessment,
    }
    return render(request, 'core/submission_grade_form.html', context)


@login_required
@user_passes_test(lambda u: is_student(u) or is_instructor(u) or is_admin(u) or u.is_superuser, login_url='/login/')
def submission_detail(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    
    if is_student(request.user) and submission.student != request.user:
        return redirect('core:student_dashboard')
    
    if is_instructor(request.user) and not submission.assessment.course.instructors.filter(pk=request.user.pk).exists() and not is_admin(request.user) and not request.user.is_superuser:
        return redirect('core:instructor_dashboard')

    context = {
        'submission': submission,
        'assessment': submission.assessment,
        'course': submission.assessment.course,
    }
    return render(request, 'core/submission_detail.html', context)


# --- Notification Management Views ---

@login_required
def all_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    # Mark all notifications on this page as read
    notifications.filter(is_read=False).update(is_read=True)

    context = {
        'notifications': notifications,
    }
    return render(request, 'core/all_notifications.html', context)


@login_required
def mark_notification_as_read(request, pk):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)
