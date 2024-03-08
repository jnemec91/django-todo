from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from todo_list_app.models import UserOptions, TodoList, TodoField
from .setup import TestSetup

class TestUserLoginView(TestCase):
    """
    Class for testing of detail view of todo list application.
    """
    
    def setUp(self) -> None:
        """
        Method for setting up test environment.
        """
        self.setup = TestSetup()
        self.client = self.setup.client
        self.another_user = self.setup.another_user
    


    def test_user_login_GET_wo_user(self):
        """
        Test user_login view without user logged in using GET method.
        Should return login page.
        """
        response = self.client.get(reverse('todo_list_app:login'))
        self.assertEquals(response.status_code, 200)
        for template in ('todo_list/login.html',
                         'todo_list/base.html',
                         'todo_list/navbar.html',
                         'todo_list/footer.html'
                         ):
            self.assertTemplateUsed(response, template)
    
    

    def test_user_login_GET_w_user(self):
        """
        Test user_login view with user logged in using GET method.
        Should redirect to index page.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('todo_list_app:login'))
        self.assertRedirects(response, reverse('todo_list_app:index'), status_code=302)
    


    def test_user_login_POST_wo_user_ok(self):
        """
        Test user_login view without user logged in using POST method.
        Should redirect to index page.
        """
        response = self.client.post(reverse('todo_list_app:login'), {'username': 'testuser', 'password': '12345'})
        self.assertRedirects(response, reverse('todo_list_app:index'), status_code=302)
    


    def test_user_login_POST_wo_user_wrong_password(self):
        """
        Test user_login view without user logged in using POST method with wrong data.
        Should return login page with error message.
        """
        response = self.client.post(reverse('todo_list_app:login'),{'username': 'testuser', 'password': 'wrong'}, follow=True)
        self.assertRedirects(response, reverse('todo_list_app:login'), status_code=302)

        messages = list(response.context.get('messages'))

        for message in messages:
            self.assertIn('error', message.tags)
            self.assertIn('You`ve entered a wrong username or password.', message.message)


        
    def test_user_login_POST_wo_user_wrong_username(self):
        """
        Test user_login view without user logged in using POST method with wrong data.
        Should return login page with error message.
        """
        response = self.client.post(reverse('todo_list_app:login'),{'username': 'wrong', 'password': '12345'}, follow=True)
        self.assertRedirects(response, reverse('todo_list_app:login'), status_code=302)

        messages = list(response.context.get('messages'))

        for message in messages:
            self.assertIn('error', message.tags)
            self.assertIn('You`ve entered a wrong username or password.', message.message)



    def test_user_login_POST_w_user(self):
        """
        Test user_login view with user logged in using POST method.
        Should return error 405.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('todo_list_app:login'), {'username': 'testuser', 'password': '12345'})
        self.assertEquals(response.status_code, 405)



    def test_user_login_PUT_wo_user(self):
        """
        Test user_login view with user logged in using POST method with wrong data.
        Should return error 405.
        """
        response = self.client.put(reverse('todo_list_app:login'), {'username': 'wrong', 'password': 'wrong'})
        self.assertEquals(response.status_code, 405)



    def test_user_login_PUT_w_user(self):
        """
        Test user_login view with user logged in using POST method with wrong data.
        Should return error 405.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.put(reverse('todo_list_app:login'), {'username': 'wrong', 'password': 'wrong'})
        self.assertEquals(response.status_code, 405)



    def test_user_login_DELETE_wo_user(self):
        """
        Test user_login view with user logged in using POST method with wrong data.
        Should return error 405.
        """
        response = self.client.delete(reverse('todo_list_app:login'), {'username': 'wrong', 'password': 'wrong'})
        self.assertEquals(response.status_code, 405)
    
    
    
    def test_user_login_DELETE_w_user(self):
        """
        Test user_login view with user logged in using POST method with wrong data.
        Should return error 405.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.delete(reverse('todo_list_app:login'), {'username': 'wrong', 'password': 'wrong'})
        self.assertEquals(response.status_code, 405)