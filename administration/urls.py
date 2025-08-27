from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
    # Dashboard
    path('', views.dashboard_view, name='dashboard'),
    
    # User management
    path('users/', views.user_list_view, name='user_list'),
    path('users/create/', views.user_create_view, name='user_create'),
    path('users/<int:user_id>/edit/', views.user_edit_view, name='user_edit'),
    path('users/<int:user_id>/toggle-status/', views.user_toggle_status_view, name='user_toggle_status'),
    path('users/<int:user_id>/delete/', views.user_delete_view, name='user_delete'),
    
    # Course management
    path('courses/', views.course_list_view, name='course_list'),
    path('courses/create/', views.course_create_view, name='course_create'),
    path('courses/<int:course_id>/edit/', views.course_edit_view, name='course_edit'),
    path('courses/<int:course_id>/delete/', views.course_delete_view, name='course_delete'),
    path('api/course-suggestions/', views.course_suggestions_api, name='course_suggestions_api'),
    
    # Exam management
    path('exams/', views.exam_list_view, name='exam_list'),
    path('exams/create/', views.exam_create_view, name='exam_create'),
    path('exams/<int:exam_id>/edit/', views.exam_edit_view, name='exam_edit'),
    path('exams/<int:exam_id>/delete/', views.exam_delete_view, name='exam_delete'),
    
    # Question management
    path('questions/', views.question_list_view, name='question_list'),
    path('questions/create/', views.question_create_view, name='question_create'),
    path('questions/<int:question_id>/edit/', views.question_edit_view, name='question_edit'),
    path('questions/<int:question_id>/preview/', views.question_preview_view, name='question_preview'),
    path('questions/<int:question_id>/delete/', views.question_delete_view, name='question_delete'),
    
    # Assignment management
    path('assignments/', views.assignment_list_view, name='assignment_list'),
    path('assignments/create/', views.assignment_create_view, name='assignment_create'),
    
    # Reports and history
    path('reports/', views.reports_view, name='reports'),
    path('history/', views.user_history_view, name='user_history'),
    
    # Exam results management
    path('exams/<int:exam_id>/results/', views.exam_results_view, name='exam_results'),
    path('user-exam/<int:user_exam_id>/detail/', views.user_exam_detail_view, name='user_exam_detail'),
    path('users/<int:user_id>/history/', views.individual_user_history_view, name='individual_user_history'),
    
    # Interface management
    path('interfaces/', views.interface_list_view, name='interface_list'),
    path('interfaces/create/', views.interface_create_view, name='interface_create'),
    path('users/<int:user_id>/interface-access/', views.user_interface_access_view, name='user_interface_access'),
    path('bulk-interface-access/', views.bulk_interface_access_view, name='bulk_interface_access'),
    
    # Export functionality
    path('users/<int:user_id>/history/export/excel/', views.export_user_history_excel, name='export_user_history_excel'),
    path('users/<int:user_id>/history/export/pdf/', views.export_user_history_pdf, name='export_user_history_pdf'),
    path('reports/export/excel/', views.export_reports_excel, name='export_reports_excel'),
    path('reports/export/pdf/', views.export_reports_pdf, name='export_reports_pdf'),
]