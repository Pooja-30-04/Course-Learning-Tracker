from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Result
from courses.models import Progress
from django.contrib import messages

@login_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)

    course = quiz.course

    lessons = course.lessons.all()
    total_lessons = lessons.count()

    completed_lessons = Progress.objects.filter(
        user=request.user,
        lesson__in=lessons,
        completed=True
    ).count()

    progress_pct = 0
    if total_lessons > 0:
        progress_pct = (completed_lessons / total_lessons) * 100


    # Restrict quiz access
    if progress_pct < 100:
        messages.error(request,
                       "Complete the entire course before attempting the quiz.")
        return redirect('courses:detail', pk=course.pk)

    questions = quiz.questions.all()

    if request.method == 'POST':
        total_questions = questions.count()
        correct_answers = 0
        for question in questions:
            selected_option = request.POST.get(str(question.id))
            if selected_option == question.correct_option:
                correct_answers += 1

        score = int((correct_answers / total_questions) * 100) if total_questions else 0
        passed = score >= quiz.passing_score

        result = Result.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            accuracy=score,
            correct_answers=correct_answers,
            total_questions=total_questions,
            passed=passed,
        )

        return redirect('quizzes:result', pk=result.pk)

    return render(request, 'quizzes/quiz_take.html', {
        'quiz': quiz,
        'questions': questions,
        'progress_pct': progress_pct,
    })

@login_required
def quiz_result(request, pk):
    result = get_object_or_404(Result, pk=pk, user=request.user)
    return render(request, 'quizzes/quiz_result.html', {'result': result})