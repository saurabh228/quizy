from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Start a new quiz session with the specified number of total_questions
    path('start_quiz/<int:total_questions>/', views.start_quiz, name='start_quiz'),

    # Quiz page for an active session
    path('quiz/<int:session_id>/', views.quiz, name='quiz'),

    # Fetch a question for the quiz session
    path('get_question/<int:session_id>/', views.get_question, name='get_question'),

    # Submit an answer for a question in the quiz session
    path('submit_answer/<int:session_id>/<int:question_id>/<str:selected_options>/', views.submit_answer, name='submit_answer'),

    # View results of a completed quiz session
    path('get_results/<int:session_id>/', views.get_results, name='get_results'),
    
    # Mark quiz session as completed
    path('complete_quiz/<int:session_id>/', views.complete_quiz, name='complete_quiz'),

    # User authentication paths
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]