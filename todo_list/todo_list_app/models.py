from django.db import models
from django.contrib.auth.models import User
import hashlib

# UserOptions model
class UserOptions(models.Model):
    """
    Model for user options, which can be changed by user in settings page.
    
    Fields:\n
        user - user, which options are stored in this model\n
        dark_mode - boolean field, which indicates if user uses dark mode\n
        email_notifications - boolean field, which indicates if user wants to receive email notifications\n
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dark_mode = models.BooleanField(default=False)

    font_style_choices = [
        ('1', 'Marck Script'),
        ('2', 'Dancing Script'),
        ('3', 'Marcellus'),
        ('4', 'Roboto Slab'),
        ('5', 'Oswald'),
    ]

    font_style = models.CharField(max_length=255, choices=font_style_choices, default='1')


    def __str__(self) -> str:
        """
        returns string representation of UserOptions object
        """
        return f'{self.user.username}`s useroptions'

# TodoList model
class TodoList(models.Model):
    """
    Model for todo list, which can be created by user and contains information about tasks.

    Fields:\n
        name - name of todo list\n
        owner - user, which created this todo list\n
        access_granted - boolean field, which indicates if users that access list via share link can edit it.\n
        fields - fields, which are in this todo list\n
        hash - hash of todo list, which is used to access todo list without authorization\n
        created_at - date and time when todo list was created\n

    Methods:\n
        _create_hash - creates hash of todo list, which is used to access todo list without authorization\n
    """
    name = models.CharField(max_length=255, null=False, blank=False)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    owner = models.ManyToManyField(User, blank=True,null=True, related_name='todo_lists')
    access_granted = models.BooleanField(default=False)
    fields = models.ManyToManyField('TodoField', blank=True)
    hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
   
    def _create_hash(self) -> str:
        """
        Creates hash of todo list, which is used to access todo list without authorization.
        """
        h = hashlib.new('sha256')
        id_bytes = bytes(str(self.id),'utf-8')
        h.update(id_bytes)
        return h.hexdigest()

    def __str__(self) -> str:
        """
        Returns string representation of TodoList object
        """
        return self.name
    

# TodoField model
class TodoField(models.Model):
    """
    Model for todo field, which can be added to todo list and contains information about task.

    Fields:\n
        name - name of todo field\n
        text - text of todo field\n
        checked - boolean field, which indicates if todo field is checked\n
        links_list - boolean field, which indicates if todo field is links list\n
        list_link - todo list, which is linked to this todo field\n
        created_at - date and time when todo field was created\n
        deadline_at - date and time when todo field should be done\n
    """
    name = models.CharField(max_length=255, null=False, blank=False)
    text = models.TextField(null=False, blank=True)
    checked = models.BooleanField(default=False)
    links_list = models.BooleanField(default=False)
    list_link = models.ForeignKey('TodoList', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline_at = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        """
        Returns string representation of TodoField object
        """
        return self.name