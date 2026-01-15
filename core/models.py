# core/models.py
from django.db import models
from django.contrib.auth.models import User
import json

class District(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Taluka(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} - {self.district.name}"
    
    class Meta:
        ordering = ['name']
        unique_together = ['name', 'district']

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class School(models.Model):
    TYPE_CHOICES = [
        ('boys', 'Boys Only'),
        ('girls', 'Girls Only'),
        ('coed', 'Co-educational'),
    ]
    
    LOCATION_CHOICES = [
        ('urban', 'Urban'),
        ('rural', 'Rural'),
    ]
    
    MEDIUM_CHOICES = [
        ('kannada', 'Kannada'),
        ('english', 'English'),
        ('marathi', 'Marathi'),
        ('urdu', 'Urdu'),
    ]
    
    udise_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    taluka = models.ForeignKey(Taluka, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    school_type = models.CharField(max_length=100)
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES)
    medium = models.CharField(max_length=10, choices=MEDIUM_CHOICES)
    
    def __str__(self):
        return f"{self.name} ({self.udise_code})"
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['taluka']),
            models.Index(fields=['udise_code']),
        ]

class Student(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    CLASS_CHOICES = [(i, f'Class {i}') for i in range(1, 11)]
    
    name = models.CharField(max_length=100)
    sts_number = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    standard = models.IntegerField(choices=CLASS_CHOICES)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} (Class {self.standard}) - {self.school.name}"
    
    class Meta:
        ordering = ['name']
        unique_together = ['sts_number', 'school']
        indexes = [
            models.Index(fields=['school', 'standard']),
            models.Index(fields=['standard']),
        ]

class Assignment(models.Model):
    CLASS_CHOICES = [(i, f'Class {i}') for i in range(1, 11)]
    
    title = models.CharField(max_length=200)
    tasks = models.JSONField(default=list)  # List of task strings
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    standard = models.IntegerField(choices=CLASS_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - Class {self.standard} ({self.subject.name})"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['standard']),
            models.Index(fields=['subject', 'standard']),
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['created_at']),
        ]

class TaskEvaluation(models.Model):
    STATUS_CHOICES = [
        ('solved', 'SOLVED'),
        ('unsolved', 'UNSOLVED'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    task_index = models.IntegerField()  # Index of task in assignment.tasks list
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unsolved')
    evaluated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    evaluated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'assignment', 'task_index']
        indexes = [
            models.Index(fields=['student', 'assignment']),
            models.Index(fields=['status']),
            models.Index(fields=['assignment', 'status']),
        ]

# Profile Extensions
class DDPIProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"DDPI: {self.user.username} - {self.district.name}"

class BEOProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    taluka = models.ForeignKey(Taluka, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"BEO: {self.user.username} - {self.taluka.name}"

class PrincipalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Principal: {self.user.username} - {self.school.name}"