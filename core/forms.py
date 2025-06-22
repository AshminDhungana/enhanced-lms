# core/forms.py

from django import forms
from .models import Course, Enrollment, UserProfile, Assessment, Submission # Corrected: Ensure this line imports models correctly
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Field

class CourseForm(forms.ModelForm):
    """
    Form for creating and updating Course objects.
    Instructors field is filtered to show only users who are instructors.
    """
    instructors = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='instructor').distinct(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select instructors for this course."
    )

    class Meta:
        model = Course
        fields = ['title', 'description', 'instructors', 'difficulty', 'price', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        help_texts = {
            'is_active': 'Check to make this course available for enrollment.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Course Details',
                Field('title', css_class='form-control'),
                Field('description', css_class='form-control'),
                Field('difficulty', css_class='form-control'),
                Field('price', css_class='form-control'),
                Field('is_active', css_class='form-check-input'),
            ),
            Fieldset(
                'Instructors',
                Field('instructors', css_class='checkbox-inline')
            ),
            Submit('submit', 'Save Course', css_class='btn btn-primary bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg')
        )
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea, forms.Select, forms.NumberInput, forms.EmailInput, forms.URLInput, forms.DateTimeInput)):
                field.widget.attrs.update({'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'})
            elif isinstance(field.widget, forms.CheckboxInput):
                 field.widget.attrs.update({'class': 'form-check-input h-4 w-4 text-indigo-600 border-gray-300 rounded'})
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({'class': 'mr-2'})


class EnrollmentForm(forms.ModelForm):
    """
    Form for enrolling a student in a course.
    """
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'is_completed', 'progress']
        widgets = {
            'progress': forms.NumberInput(attrs={'step': 0.01, 'min': 0, 'max': 100}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Enrollment Details',
                Field('student', css_class='form-control'),
                Field('course', css_class='form-control'),
                Field('is_completed', css_class='form-check-input'),
                Field('progress', css_class='form-control'),
            ),
            Submit('submit', 'Save Enrollment', css_class='btn btn-primary bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg')
        )
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea, forms.Select, forms.NumberInput)):
                field.widget.attrs.update({'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'})
            elif isinstance(field.widget, forms.CheckboxInput):
                 field.widget.attrs.update({'class': 'form-check-input h-4 w-4 text-indigo-600 border-gray-300 rounded'})


class AssessmentForm(forms.ModelForm):
    """
    Form for creating and updating Assessment objects.
    """
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'], # Format for datetime-local input
        help_text="Format: YYYY-MM-DD HH:MM (e.g., 2025-07-25 14:30)"
    )

    class Meta:
        model = Assessment
        fields = ['course', 'title', 'description', 'assessment_type', 'due_date', 'max_score']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('course', css_class='form-control'),
            Field('title', css_class='form-control'),
            Field('description', css_class='form-control'),
            Field('assessment_type', css_class='form-control'),
            Field('due_date', css_class='form-control'),
            Field('max_score', css_class='form-control'),
            Submit('submit', 'Save Assessment', css_class='btn btn-primary bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg')
        )
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea, forms.Select, forms.NumberInput, forms.DateTimeInput)):
                field.widget.attrs.update({'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'})


class SubmissionGradingForm(forms.ModelForm):
    """
    Form for instructors to grade a student's submission.
    """
    class Meta:
        model = Submission
        fields = ['score', 'feedback', 'is_graded']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 3}),
            'score': forms.NumberInput(attrs={'step': 0.01, 'min': 0}),
        }
        help_texts = {
            'is_graded': 'Check this box after providing the score and feedback.',
        }

    def __init__(self, *args, **kwargs):
        # Pass max_score from the assessment to the form for validation
        self.assessment_max_score = kwargs.pop('assessment_max_score', None)
        super().__init__(*args, **kwargs)
        if self.assessment_max_score is not None:
            self.fields['score'].widget.attrs['max'] = self.assessment_max_score

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('score', css_class='form-control'),
            Field('feedback', css_class='form-control'),
            Field('is_graded', css_class='form-check-input'),
            Submit('submit', 'Save Grade', css_class='btn btn-primary bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg')
        )
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea, forms.Select, forms.NumberInput)):
                field.widget.attrs.update({'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input h-4 w-4 text-indigo-600 border-gray-300 rounded'})

    def clean_score(self):
        score = self.cleaned_data['score']
        if self.assessment_max_score is not None and score is not None and score > self.assessment_max_score:
            raise forms.ValidationError(f"Score cannot exceed maximum score of {self.assessment_max_score}.")
        return score
