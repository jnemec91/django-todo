from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from todo_list_app.models import  UserOptions, TodoList, TodoField


class TestSetup:
    """
    Class for setting up tests.
    """

    def __init__(self) -> None:
        # create standart user
        self.user = User.objects.create_user(
            email='test@test.com',
            username='testuser',
            first_name='test',
            last_name='test',
            password='12345',
            )
        
        self.user_options = UserOptions.objects.create(
            user=self.user,
            dark_mode=False,
            font_style='1',
            )
        

        # create another user
        self.another_user = User.objects.create_user(
            email='another@test.com',
            username='anotheruser',
            first_name='another',
            last_name='another',
            password='12345',
            )
        
        self.user_options = UserOptions.objects.create(
            user=self.another_user,
            dark_mode=False,
            font_style='1',
            )

        

        
        # create django test client
        self.client =  Client()