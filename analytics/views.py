from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quizzes.models import Result
from courses.models import Progress, Enrollment
from django.db.models import Avg, Count
import json

@login_required
def analytics_dashboard(request):
    user = request.user
    
    # Overview
    results = Result.objects.filter(user=user).order_by('timestamp')
    total_tests = results.count()
    passed_tests = results.filter(passed=True).count()
    
    overall_accuracy = 0
    if total_tests > 0:
        overall_accuracy = sum(r.accuracy for r in results) / total_tests
        
    # Chart Data
    chart_labels = [r.quiz.title for r in results]
    chart_scores = [r.score for r in results]
    
    # Weak Topics (Scores < 100)
    weak_results = results.filter(score__lt=100)
    
    context = {
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'overall_accuracy': round(overall_accuracy, 1),
        'chart_labels': json.dumps(chart_labels),
        'chart_scores': json.dumps(chart_scores),
        'weak_results': weak_results,
    }
    
    return render(request, 'analytics/dashboard.html', context)
