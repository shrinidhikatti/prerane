# core/forms.py
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import (
    District, Taluka, Subject, School, Student, Assignment, 
    DDPIProfile, BEOProfile, PrincipalProfile, TaskEvaluation
)

class TalukaForm(forms.ModelForm):
    class Meta:
        model = Taluka
        fields = ['name', 'district']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'district': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        }

class BEOCreationForm(UserCreationForm):
    taluka = forms.ModelChoiceField(queryset=Taluka.objects.all(), required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        district = kwargs.pop('district', None)
        super().__init__(*args, **kwargs)
        if district:
            self.fields['taluka'].queryset = Taluka.objects.filter(district=district)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'})

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['udise_code', 'name', 'taluka', 'type', 'school_type', 'location', 'medium']
        widgets = {
            'udise_code': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'taluka': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'type': forms.RadioSelect(attrs={'class': 'mr-2'}),
            'school_type': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'location': forms.RadioSelect(attrs={'class': 'mr-2'}),
            'medium': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        }
    
    def __init__(self, *args, **kwargs):
        taluka = kwargs.pop('taluka', None)
        super().__init__(*args, **kwargs)
        if taluka:
            self.fields['taluka'].queryset = Taluka.objects.filter(id=taluka.id)

class PrincipalCreationForm(UserCreationForm):
    school = forms.ModelChoiceField(queryset=School.objects.all(), required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        taluka = kwargs.pop('taluka', None)
        super().__init__(*args, **kwargs)
        if taluka:
            self.fields['school'].queryset = School.objects.filter(taluka=taluka)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'})

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'sts_number', 'gender', 'standard']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'sts_number': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'gender': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'standard': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        }

class AssignmentForm(forms.ModelForm):
    tasks = forms.CharField(
        widget=forms.HiddenInput(),
        help_text="Add tasks using the interface below"
    )
    
    class Meta:
        model = Assignment
        fields = ['title', 'tasks', 'subject', 'standard', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'subject': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'standard': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'start_date': forms.DateInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'type': 'date'}),
        }
    
    def clean_tasks(self):
        tasks_text = self.cleaned_data['tasks']
        tasks_list = [task.strip() for task in tasks_text.split('\n') if task.strip()]
        return tasks_list

class TaskEvaluationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        assignment = kwargs.pop('assignment')
        students = kwargs.pop('students')
        super().__init__(*args, **kwargs)
        
        for student in students:
            for i, task in enumerate(assignment.tasks):
                field_name = f'student_{student.id}_task_{i}'
                try:
                    evaluation = TaskEvaluation.objects.get(
                        student=student, 
                        assignment=assignment, 
                        task_index=i
                    )
                    initial_value = evaluation.status
                except TaskEvaluation.DoesNotExist:
                    initial_value = 'unsolved'
                
                self.fields[field_name] = forms.ChoiceField(
                    choices=[('solved', 'SOLVED'), ('unsolved', 'UNSOLVED')],
                    widget=forms.RadioSelect(attrs={'class': 'mr-2'}),
                    initial=initial_value,
                    required=False
                )

class PrincipalUpdateForm(forms.ModelForm):
    new_password = forms.CharField(
        max_length=128,
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'Leave empty to keep current password'
        }),
        help_text="Leave empty to keep the current password"
    )
    
    class Meta:
        model = PrincipalProfile
        fields = ['school']
        widgets = {
            'school': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        }
    
    def __init__(self, *args, **kwargs):
        taluka = kwargs.pop('taluka', None)
        super().__init__(*args, **kwargs)
        if taluka:
            self.fields['school'].queryset = School.objects.filter(taluka=taluka)

class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'Current Password'
        }),
        help_text="Enter your current password"
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'New Password'
        }),
        help_text="Enter your new password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'Confirm New Password'
        }),
        help_text="Confirm your new password"
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        if self.user and not self.user.check_password(current_password):
            raise forms.ValidationError("Current password is incorrect.")
        return current_password
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("New passwords don't match.")
        
        return cleaned_data

class ReportFilterForm(forms.Form):
    CLASS_CHOICES = [('', 'All Classes')] + [(i, f'Class {i}') for i in range(1, 11)]
    
    standard = forms.ChoiceField(choices=CLASS_CHOICES, required=False, widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}))
    taluka = forms.ModelChoiceField(queryset=Taluka.objects.all(), required=False, empty_label="All Talukas", widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}))
    school = forms.ModelChoiceField(queryset=School.objects.all(), required=False, empty_label="All Schools", widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}))
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), required=False, empty_label="All Subjects", widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}))
    assignment = forms.ModelChoiceField(queryset=Assignment.objects.all(), required=False, empty_label="All Assignments", widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}))
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'type': 'date'}))
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            if user.groups.filter(name='Principal').exists():
                principal_profile = PrincipalProfile.objects.get(user=user)
                self.fields['school'].queryset = School.objects.filter(id=principal_profile.school.id)
                self.fields['taluka'].queryset = Taluka.objects.filter(id=principal_profile.school.taluka.id)
            elif user.groups.filter(name='BEO').exists():
                beo_profile = BEOProfile.objects.get(user=user)
                self.fields['school'].queryset = School.objects.filter(taluka=beo_profile.taluka)
                self.fields['taluka'].queryset = Taluka.objects.filter(id=beo_profile.taluka.id)
            elif user.groups.filter(name='DDPI').exists():
                ddpi_profile = DDPIProfile.objects.get(user=user)
                self.fields['taluka'].queryset = Taluka.objects.filter(district=ddpi_profile.district)
                self.fields['school'].queryset = School.objects.filter(taluka__district=ddpi_profile.district)