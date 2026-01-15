# core/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Authentication
    path('', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # DDPI URLs
    path('ddpi/talukas/', views.ManageTalukaListView.as_view(), name='manage_talukas'),
    path('ddpi/talukas/create/', views.ManageTalukaCreateView.as_view(), name='create_taluka'),
    path('ddpi/talukas/<int:pk>/update/', views.ManageTalukaUpdateView.as_view(), name='update_taluka'),
    path('ddpi/talukas/<int:pk>/delete/', views.ManageTalukaDeleteView.as_view(), name='delete_taluka'),
    
    path('ddpi/subjects/', views.ManageSubjectListView.as_view(), name='manage_subjects'),
    path('ddpi/subjects/create/', views.ManageSubjectCreateView.as_view(), name='create_subject'),
    path('ddpi/subjects/<int:pk>/update/', views.ManageSubjectUpdateView.as_view(), name='update_subject'),
    path('ddpi/subjects/<int:pk>/delete/', views.ManageSubjectDeleteView.as_view(), name='delete_subject'),
    
    path('ddpi/beos/', views.ManageBEOListView.as_view(), name='manage_beos'),
    path('ddpi/beos/create/', views.ManageBEOCreateView.as_view(), name='create_beo'),
    path('ddpi/beos/<int:pk>/update/', views.ManageBEOUpdateView.as_view(), name='update_beo'),
    path('ddpi/beos/<int:pk>/delete/', views.ManageBEODeleteView.as_view(), name='delete_beo'),
    
    path('ddpi/assignments/', views.ManageAssignmentListView.as_view(), name='manage_assignments'),
    path('ddpi/assignments/create/', views.ManageAssignmentCreateView.as_view(), name='create_assignment'),
    path('ddpi/assignments/<int:pk>/update/', views.ManageAssignmentUpdateView.as_view(), name='update_assignment'),
    path('ddpi/assignments/<int:pk>/delete/', views.ManageAssignmentDeleteView.as_view(), name='delete_assignment'),
    
    # BEO URLs
    path('beo/schools/', views.ManageSchoolListView.as_view(), name='manage_schools'),
    path('beo/schools/create/', views.ManageSchoolCreateView.as_view(), name='create_school'),
    path('beo/schools/<int:pk>/update/', views.ManageSchoolUpdateView.as_view(), name='update_school'),
    path('beo/schools/<int:pk>/delete/', views.ManageSchoolDeleteView.as_view(), name='delete_school'),
    
    path('beo/principals/', views.ManagePrincipalListView.as_view(), name='manage_principals'),
    path('beo/principals/create/', views.ManagePrincipalCreateView.as_view(), name='create_principal'),
    path('beo/principals/<int:pk>/update/', views.ManagePrincipalUpdateView.as_view(), name='update_principal'),
    path('beo/principals/<int:pk>/delete/', views.ManagePrincipalDeleteView.as_view(), name='delete_principal'),
    
    # Principal URLs
    path('principal/students/', views.ManageStudentListView.as_view(), name='manage_students'),
    path('principal/students/create/', views.ManageStudentCreateView.as_view(), name='create_student'),
    path('principal/students/<int:pk>/update/', views.ManageStudentUpdateView.as_view(), name='update_student'),
    path('principal/students/<int:pk>/delete/', views.ManageStudentDeleteView.as_view(), name='delete_student'),
    
    path('principal/assignments/', views.EvaluateAssignmentListView.as_view(), name='assignment_evaluations'),
    path('principal/assignments/<int:pk>/evaluate/', views.EvaluateAssignmentView.as_view(), name='evaluate_assignment'),

    path('reports/', views.GenerateReportView.as_view(), name='reports'),
    path('change-password/', views.PasswordChangeView.as_view(), name='password_change'),
]
