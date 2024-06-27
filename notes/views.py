from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from .models import Activity, Grade

class LoginView(View):
    def get(self, request):
        return render(request, 'notes/login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('activities')
        else:
            return render(request, 'notes/login.html', {'error': 'Invalid email or password'})

class ActivitiesView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        user = request.user
        activities = Activity.objects.all()
        grades = Grade.objects.filter(user=user)

        grades_by_module = {}
        for activity in activities:
            grades_by_module.setdefault(activity.module, []).append(
                {'activity': activity, 'grade': grades.filter(activity=activity).first()}
            )

        return render(request, 'notes/activities.html', {'grades_by_module': grades_by_module})

def update_grade(request):
    if request.method == 'POST':
        activity_id = request.POST.get('activity_id')
        grade_id = request.POST.get('grade_id')
        ontime = int(request.POST.get('ontime', 0))  # Proporciona un valor predeterminado
        quality = int(request.POST.get('quality', 0))  # Proporciona un valor predeterminado
        grade_value = 10 - (ontime + quality)
        user = request.user

        if grade_id and grade_id != 'null':
            grade = get_object_or_404(Grade, id=grade_id, user=user)
            grade.grade = grade_value
        else:
            activity = get_object_or_404(Activity, id=activity_id)
            grade, created = Grade.objects.get_or_create(user=user, activity=activity, defaults={'grade': grade_value})
            if not created:
                grade.grade = grade_value
        
        if 'screenshot' in request.FILES:
            grade.screenshot = request.FILES['screenshot']
        
        grade.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

def redirect_to_login(request):
    return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('login')
