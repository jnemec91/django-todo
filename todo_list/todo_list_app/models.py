from django.db import models
from django.contrib.auth.models import User

# UserOptions model
class UserOptions(models.Model):
    """Model for user options, which can be changed by user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dark_mode = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user.username}`s useroptions'

# TodoList model
class TodoList(models.Model):
    """Model for todo list, which can be created by user and contains todo fields"""
    name = models.CharField(max_length=255, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    access_granted = models.ManyToManyField(User, related_name='access_granted', blank=True)
    fields = models.ManyToManyField('TodoField', blank=True)

    def __str__(self) -> str:
        return self.name

# TodoField model
class TodoField(models.Model):
    """Model for todo field, which can be added to todo list and contains information about task"""
    name = models.CharField(max_length=255, null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    checked = models.BooleanField(default=False)
    links_list = models.BooleanField(default=False)
    list_link = models.ForeignKey('TodoList', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name