from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Issue, Comment
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    pending = Issue.objects.filter(status='pending')
    closed = Issue.objects.filter(status='closed')
    my_issues = Issue.objects.filter(owner=request.user)
    return render(request, 'forum_app/dashboard.html', {
        'pending': pending,
        'closed': closed,
        'my_issues': my_issues,
    })

@login_required
def create_issue(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        Issue.objects.create(title=title, description=description, owner=request.user)
        return redirect('dashboard')
    return render(request, 'forum_app/create_issue.html')

@login_required
def issue_detail(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == 'POST':
        if issue.status == 'closed':
            return HttpResponseForbidden("Cannot comment on closed issues.")
        Comment.objects.create(
            issue=issue, author=request.user, content=request.POST['content']
        )
        return redirect('issue_detail', pk=pk)
    return render(request, 'forum_app/issue_detail.html', {'issue': issue})

@login_required
def close_issue(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if request.user != issue.owner:
        return HttpResponseForbidden("Only the issue owner can close it.")
    issue.status = 'closed'
    issue.save()
    return redirect('dashboard')
