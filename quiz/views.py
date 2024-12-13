from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
import random

from .models import QuizSession, Question, SessionQuestion

def home(request):
    """
    View for the home page.
    Displays a form to start a new quiz and lists previous sessions.
    """
    if request.user.is_authenticated:
        # Fetch user's quiz sessions ordered by most recent
        sessions = QuizSession.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'quiz/home.html', {'sessions': sessions})
    else:
        return render(request, 'quiz/home.html')

@login_required
def start_quiz(request, total_questions):
    """
    Starts a new quiz session with the specified number of questions.
    """
    try:
        total_questions = int(total_questions)
        if total_questions <= 0:
            raise ValueError("Number of questions must be a positive integer.")
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('home')

    # Create a new quiz session for the user
    session = QuizSession.objects.create(user=request.user, total_questions=total_questions)
    return JsonResponse({'session_id': session.id})

@login_required
def quiz(request, session_id):
    """
    View for the quiz page.
    Displays the quiz interface if the session is valid.
    """
    session = get_object_or_404(QuizSession, id=session_id, user=request.user)
    if session.is_completed:
        messages.error(request, 'This quiz session has already been completed.')
        return redirect('home')

    context = {
        'session': session,
        'total_questions': session.total_questions,
        'completed_questions': session.completed_questions,
    }
    return render(request, 'quiz/quiz.html', context)

@login_required
def get_question(request, session_id):
    """
    Retrieves the next question for the quiz session.
    """
    session = get_object_or_404(QuizSession, id=session_id, user=request.user)

    if session.is_completed:
        return JsonResponse({'error': 'Quiz is already completed.'}, status=400)

    # If there's a current question, continue with it
    if session.current_question:
        question = session.current_question
    else:
        # Get unanswered questions
        answered_questions = session.session_questions.values_list('question_id', flat=True)
        remaining_questions = Question.objects.exclude(id__in=answered_questions)

        if not remaining_questions.exists():
            # No more questions currently in the database;
            return JsonResponse({'error': 'No more questions at the moment. Please Resume quiz later'}, status=200)

        # Randomly select the next question
        question = random.choice(remaining_questions)
        session.current_question = question
        session.save()

    question_data = {
        'question_id': question.id,
        'question_text': question.question_text,
        'options': [question.option1, question.option2, question.option3, question.option4],
        'type': question.question_type,
        'completed_questions': session.completed_questions,
        'total_questions': session.total_questions,
    }

    return JsonResponse(question_data)

@login_required
def submit_answer(request, session_id, question_id, selected_options):
    """
    Submits the user's answer for a question and updates the quiz session.
    """
    session = get_object_or_404(QuizSession, id=session_id, user=request.user)
    question = get_object_or_404(Question, id=question_id)

    if session.is_completed:
        return JsonResponse({'error': 'Quiz is already completed.'}, status=400)

    # Check if question has already been answered in this session
    if SessionQuestion.objects.filter(session=session, question=question).exists():
        return JsonResponse({'error': 'Question already answered.'}, status=400)

    # Process selected options
    selected_options_list = selected_options.split(',')
    selected_options_set = set(selected_options_list)
    if not selected_options_set:
        return JsonResponse({'error': 'No options selected.'}, status=400)

    correct_options_set = set(question.correct_options)
    score = 0.0

    # Evaluate the answer
    if selected_options_set == correct_options_set:
        session.correct_answers += 1
        result = 'correct'
        score = 1.0
    elif selected_options_set.issubset(correct_options_set):
        session.partially_correct_answers += 1
        result = 'partial'
        score = round(len(selected_options_set & correct_options_set) / len(correct_options_set), 2)
    else:
        session.incorrect_answers += 1
        result = 'incorrect'

    # Update session score and progress
    session.score += score
    session.completed_questions += 1
    session.current_question = None

    # Check if quiz is completed
    if session.completed_questions >= session.total_questions:
        session.is_completed = True

    session.save()

    # Save user's selected options for the question
    SessionQuestion.objects.create(
        session=session,
        question=question,
        selected_options=selected_options_list,
        score=score,
    )

    response_data = {
    #     'result': result,
    #     'marks': score,
    #     'total_score': session.score,
        'completed_questions': session.completed_questions,
        'total_questions': session.total_questions,
    }

    return JsonResponse(response_data)

@login_required
def complete_quiz(request, session_id):
    """
    Marks the quiz session as complete.
    """
    session = get_object_or_404(QuizSession, id=session_id, user=request.user)

    if session.is_completed:
        return JsonResponse({'status': 'Quiz completed successfully.'})

    # Mark the quiz as completed
    session.is_completed = True
    session.save()

    return JsonResponse({'status': 'Quiz completed successfully.'})

@login_required
def get_results(request, session_id):
    """
    Displays the results of the completed quiz session.
    """
    session = get_object_or_404(QuizSession, id=session_id, user=request.user)

    if not session.is_completed:
        messages.error(request, 'Please complete the quiz to view the results.')
        return redirect('home')

    # Fetch the user's answers and related questions
    session_questions = SessionQuestion.objects.filter(session=session).select_related('question')

    questions_data = []
    for session_question in session_questions:
        question = session_question.question
        options = [question.option1, question.option2, question.option3, question.option4]
        correct_options = set(question.correct_options)
        selected_options = set(session_question.selected_options)

        questions_data.append({
            'question_text': question.question_text,
            'options': options,
            'correct_options': correct_options,
            'selected_options': selected_options,
            'score': session_question.score,
        })

    context = {
        'session': session,
        'questions_data': questions_data,
        'total_score': session.score,
        'total_questions': session.total_questions,
        'correct_answers': session.correct_answers,
        'incorrect_answers': session.incorrect_answers,
        'partially_correct_answers': session.partially_correct_answers,
    }

    return render(request, 'quiz/results.html', context)

def login_view(request):
    """
    Handles user login.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):
    """
    Logs out the current user.
    """
    logout(request)
    return redirect('home')

def register(request):
    """
    Handles new user registration.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Create new user
            form.save()
            new_user = form.save()
            login(request, new_user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})