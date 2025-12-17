from django.contrib import admin
from .models import Issue, Comment

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('issue', "content", 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)