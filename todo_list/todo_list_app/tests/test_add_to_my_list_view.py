from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from todo_list_app.models import UserOptions, TodoList, TodoField
from .setup import TestSetup
from datetime import date

class TestAddToMyListkView(TestCase):
    """
    Class for testing add to my list view of todo list application.
    """
    
    def setUp(self) -> None:
        """
        Method for setting up test environment.
        """
        self.setup = TestSetup()
        self.client = self.setup.client
        self.user = self.setup.user
        self.another_user = self.setup.another_user
        
        # create users todo list
        self.user_todo_list = TodoList.objects.create(name='todo list',
                                            created_by=self.user,
                                            access_granted=False)
        self.user_todo_list.owner.add(self.user)
        self.user_todo_list.hash = self.user_todo_list._create_hash()
        self.user_todo_list.save()

        self.todo_field = TodoField.objects.create(name='todo field',
                                                   text = 'text',
                                                   created_at = date.today(),
                                                   deadline_at = date.today(),
                                                   checked=False)
        
        self.user_todo_list.fields.add(self.todo_field)
        self.user_todo_list.save()

        # create another users todo list
        self.another_todo_list = TodoList.objects.create(name='another_list',
                                            created_by=self.another_user,
                                            access_granted=False)
        self.another_todo_list.owner.add(self.another_user)
        self.another_todo_list.owner.add(self.user)
        self.another_todo_list.hash = self.another_todo_list._create_hash()
        self.another_todo_list.save()

        self.another_todo_field = TodoField.objects.create(name='todo field',
                                                   text = 'text',
                                                   created_at = date.today(),
                                                   deadline_at = date.today(),
                                                   checked=False)

        self.another_todo_list.fields.add(self.another_todo_field)
        self.another_todo_list.save()
