from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Issue, Comment
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView

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

class CustomLoginView(LoginView):
    """
    Renders the standard AuthenticationForm as `form`
    AND injects a blank signup form as `signup_form`.
    """
    template_name = 'registration/login.html'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault('signup_form', UserCreationForm())
        return ctx

def signup(request):
    """
    Handle POST from the signup form shown on the login page.
    On success: create user, log them in, redirect to dashboard.
    On errors: re-render the same login page with form errors visible.
    """
    if request.method != 'POST':
        # For direct GET to /accounts/signup/, just bounce to login page
        return redirect('login')

    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        auth_login(request, user)
        return redirect('dashboard')

    # If invalid, re-render login page with both forms, showing signup errors
    login_form = AuthenticationForm(request=request)
    return render(
        request,
        'registration/login.html',
        {'form': login_form, 'signup_form': form},
    )