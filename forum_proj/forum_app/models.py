from django.db import models
from django.contrib.auth.models import User

class Issue(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('closed', 'Closed'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # keep issue if user deleted
        null=True,
        blank=True,
        related_name='issues'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        owner_name = self.owner.username if self.owner else "Publisher deleted"
        return f"{self.title} ({self.status}) by {owner_name}"


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        author_name = self.author.username if self.author else "Deleted user"
        return f"Comment by {author_name}"
