from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Homework, Doubt, Assignment, StudentProfile

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Default to no profile or default profile logic if needed
            if not StudentProfile.objects.filter(user=user).exists():
                StudentProfile.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard_view(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    
    if profile.is_teacher:
        assignments = Assignment.objects.filter(created_by=request.user).order_by('-created_at')
        submissions = Homework.objects.all().order_by('-created_at') # Teacher sees all? Or specific. Let's show all for now.
        return render(request, 'teacher_dashboard.html', {'assignments': assignments, 'submissions': submissions})
    else:
        # Student View
        assignments = Assignment.objects.all().order_by('-created_at')
        my_submissions = Homework.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'student_dashboard.html', {'assignments': assignments, 'my_submissions': my_submissions})

@login_required
def create_assignment(request):
    if not request.user.studentprofile.is_teacher:
        return redirect('dashboard')
        
    if request.method == 'POST':
        subject = request.POST.get('subject')
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        if not due_date:
            due_date = None
            
        gdrive_link = request.POST.get('gdrive_link')
        file = request.FILES.get('file')
        
        Assignment.objects.create(
            subject=subject,
            title=title, 
            description=description, 
            due_date=due_date, 
            gdrive_link=gdrive_link,
            file=file,
            created_by=request.user
        )
        messages.success(request, 'Assignment created successfully!')
        
    return redirect('dashboard')

@login_required
def delete_assignment(request, assignment_id):
    if not request.user.studentprofile.is_teacher:
        return redirect('dashboard')
        
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if assignment.created_by == request.user:
        assignment.delete()
        messages.success(request, 'Assignment deleted successfully!')
    
    return redirect('dashboard')

@login_required
def submit_homework(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        gdrive_link = request.POST.get('gdrive_link')
        assignment_id = request.POST.get('assignment_id')
        
        assignment = None
        if assignment_id:
            assignment = get_object_or_404(Assignment, id=assignment_id)

        if file or gdrive_link:
            # Create HW object
            hw = Homework(user=request.user)
            if assignment:
                hw.assignment = assignment
            
            if file:
                hw.file = file
                
            if gdrive_link:
                hw.gdrive_link = gdrive_link
            
            hw.save()
            
            messages.success(request, 'Homework submitted successfully!')
            return redirect('dashboard')
            
    return redirect('dashboard')

@login_required
def upload_checked_copy(request, homework_id):
    if not request.user.studentprofile.is_teacher:
        return redirect('dashboard')
        
    if request.method == 'POST':
        hw = get_object_or_404(Homework, id=homework_id)
        checked_file = request.FILES.get('checked_file')
        remarks = request.POST.get('remarks')
        checked_gdrive_link = request.POST.get('checked_gdrive_link')
        
        if checked_file:
            hw.checked_file = checked_file
            
        if checked_gdrive_link:
            hw.checked_gdrive_link = checked_gdrive_link
        
        if remarks:
            hw.remarks = remarks
            
        hw.save()
        messages.success(request, 'Checked copy uploaded!')
        
    return redirect('dashboard')

@login_required
def ask_doubt(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        file = request.FILES.get('file')
        
        if description:
            Doubt.objects.create(user=request.user, description=description, file=file)
            messages.success(request, 'Doubt submitted successfully!')
            
    return redirect('dashboard')
