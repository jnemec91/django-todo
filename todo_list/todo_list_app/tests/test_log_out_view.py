from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from todo_list_app.models import UserOptions, TodoList, TodoField
from .setup import TestSetup

class TestLogOutView(TestCase):
    """
    Class for testing of log out view of todo list application.
    """


    def setUp(self) -> None:
        """
        Method for setting up test environment.
        """
        self.setup = TestSetup()
        self.client = self.setup.client

    

    def test_log_out_GET_with_user_logged_in(self):
        """
        Test for GET request to log out view with user logged in.
        """

        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('todo_list_app:logout'))
        self.assertRedirects(response, reverse('todo_list_app:login'), status_code=302)
        self.assertFalse(self.client.session.has_key('_auth_user_id'))



    def test_log_out_GET_with_user_not_logged_in(self):
        """
        Test for GET request to log out view with user not logged in.
        """

        response = self.client.get(reverse('todo_list_app:logout'))
        self.assertRedirects(response,f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:logout') }", status_code=302)