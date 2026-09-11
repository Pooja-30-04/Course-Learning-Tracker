from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Enrollment, Progress

@login_required
def course_list(request):
    courses = Course.objects.all()
    # Annotate with enrollment status if needed
    context = {'courses': courses}
    return render(request, 'courses/course_list.html', context)

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)

    lessons = course.lessons.all()

    is_enrolled = Enrollment.objects.filter(
        user=request.user,
        course=course
    ).exists()

    quiz = None
    progress_pct = 0
    if is_enrolled:
        total_lessons = lessons.count()
        if total_lessons > 0:
            completed_lessons = Progress.objects.filter(
                user=request.user,
                lesson__in=lessons,
                completed=True
            ).count()
            progress_pct = int((completed_lessons / total_lessons) * 100)
        quiz = course.quizzes.first()
    context = {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
        'progress_pct': progress_pct,
        'quiz': quiz,
    }

    return render(request,
                 'courses/course_detail.html',
                 context)
@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('courses:detail', pk=pk)

@login_required
def lesson_detail(request, course_pk, lesson_pk):
    course = get_object_or_404(Course, pk=course_pk)
    lesson = get_object_or_404(Lesson, pk=lesson_pk, course=course)
    
    # Check enrollment
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        return redirect('courses:detail', pk=course_pk)
        
    progress, created = Progress.objects.get_or_create(user=request.user, lesson=lesson)
    
    if request.method == 'POST':
        if 'mark_complete' in request.POST:
            progress.completed = True
            progress.save()
            return redirect('courses:detail', pk=course_pk)
            
    context = {
        'course': course,
        'lesson': lesson,
        'progress': progress,
    }
    return render(request, 'courses/lesson_detail.html', context)