from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from todo_list_app.models import UserOptions, TodoList, TodoField
from .setup import TestSetup

class TestSignUpView(TestCase):
    """
    Class for testing of detail view of todo list application.
    """
    
    def setUp(self) -> None:
        """
        Method for setting up test environment.
        """
        self.setup = TestSetup()
        self.client = self.setup.client



    def test_signup_GET_wo_user(self):
        """
        Test signup view without user logged in using GET method.
        Should return signup page.
        """
        response = self.client.get(reverse('todo_list_app:signup'))
        self.assertEquals(response.status_code, 200)

        for template in ('todo_list/signup.html',
                         'todo_list/base.html',
                         'todo_list/navbar.html',
                         'todo_list/footer.html'
                         ):
            self.assertTemplateUsed(response, template)

    

    def test_signup_GET_w_user(self):
        """
        Test signup view with user logged in using GET method.
        Should redirect to index page.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('todo_list_app:signup'))
        self.assertRedirects(response, reverse('todo_list_app:index'), status_code=302)

    
    
    def test_signup_POST_wo_user(self):
        """
        Test signup view without user logged in using POST method.
        Should create new user and redirect to login page.
        """
        response = self.client.post(reverse('todo_list_app:signup'),
                                    {'username': 'newuser',
                                     'first_name': 'new',
                                     'last_name': 'user',
                                     'email': 'newuser@test.com',
                                     'password': 'newpassword',
                                     'password2': 'newpassword'
                                    })
        self.assertRedirects(response, reverse('todo_list_app:login'), status_code=302)



    def test_signup_POST_w_user(self):
        """
        Test signup view with user logged in using POST method.
        Should return method not allowed.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('todo_list_app:signup'),
                                    {'username': 'newuser',
                                     'first_name': 'new',
                                     'last_name': 'user',
                                     'email': 'newuser@test.com',
                                     'password': 'newpassword',
                                     'password2': 'newpassword'
                                    })
        self.assertEquals(response.status_code, 405)



    def test_signup_POST_wo_user_bad_password(self):
        """
        Test signup view without user logged in using POST method with bad password.
        Should redirect to signup page with error message.
        """
        response = self.client.post(reverse('todo_list_app:signup'),
                                    {'username': 'newuser',
                                     'first_name': 'new',
                                     'last_name': 'user',
                                     'email': 'newuser@test.com',
                                     'password': 'newpassword',
                                     'password2': 'badpassword'
                                    },
                                    follow=True)
        
        self.assertRedirects(response, reverse('todo_list_app:signup'), status_code=302)

        messages = list(response.context.get('messages'))
        for message in messages:
            self.assertIn('error', message.tags)
            self.assertIn('Passwords do not match.', message.message)



    def test_signup_POST_wo_user_existing_username(self):
        """
        Test signup view without user logged in using POST method with existing username.
        Should redirect to signup page with error message.
        """
        response = self.client.post(reverse('todo_list_app:signup'),
                                    {'username': 'testuser',
                                     'first_name': 'new',
                                     'last_name': 'user',
                                     'email': 'newuser@test.com',
                                     'password': 'newpassword',
                                     'password2': 'newpassword'
                                    },
                                    follow=True)
        
        self.assertRedirects(response, reverse('todo_list_app:signup'), status_code=302)

        messages = list(response.context.get('messages'))
        for message in messages:
            self.assertIn('error', message.tags)
            self.assertIn('This username already exists.', message.message)



    def test_signup_POST_wo_user_existing_email(self):
        """
        Test signup view without user logged in using POST method with existing email.
        Should return signup page with error message.
        """
        response = self.client.post(reverse('todo_list_app:signup'),
                                    {'username': 'newuser',
                                     'first_name': 'new',
                                     'last_name': 'user',
                                     'email': 'test@test.com',
                                     'password': 'newpassword',
                                     'password2': 'newpassword'
                                    },
                                    follow=True)
        
        self.assertRedirects(response, reverse('todo_list_app:signup'), status_code=302)

        messages = list(response.context.get('messages'))
        for message in messages:
            self.assertIn('error', message.tags)
            self.assertIn('Account with this email already exists.', message.message)



    def test_signup_POST_wo_user_invalid_email(self):
        """
        Test signup view without user logged in using POST method with invalid data.
        Should redirect to signup page with error message.
        """
        response = self.client.post(reverse('todo_list_app:signup'),
                                    {'username': 'newuser',
                                     'first_name': 'new',
                                     'last_name': 'user',
                                     'email': 'invalidemail',
                                     'password': 'newpassword',
                                     'password2': 'newpassword'
                                    },
                                    follow=True)
        
        self.assertRedirects(response, reverse('todo_list_app:signup'), status_code=302)

        messages = list(response.context.get('messages'))
        for message in messages:
            self.assertIn('error', message.tags)
            self.assertIn( 'Invalid email.', message.message)



    def test_signup_POST_wo_user_invalid_username(self):
        """
        Test signup view without user logged in using POST method with invalid data.
        Should redirect to signup page with error message.
        """
        response = self.client.post(reverse('todo_list_app:signup'),
                                    {'username': 'new user',
                                     'first_name': 'new',
                                     'last_name': 'user',
                                     'email': 'newuser@test.com',
                                     'password': 'newpassword',
                                     'password2': 'newpassword'
                                    },
                                    follow=True)
        
        self.assertRedirects(response, reverse('todo_list_app:signup'), status_code=302)

        messages = list(response.context.get('messages'))
        for message in messages:
            self.assertIn('error', message.tags)
            self.assertIn('Invalid username. Username can only contain letters, numbers and underscores.', message.message)
        


    def test_signup_PUT_wo_user(self):
        """
        Test signup view without user logged in using PUT method.
        Should return method not allowed.
        """
        response = self.client.put(reverse('todo_list_app:signup'))
        self.assertEquals(response.status_code, 405)



    def test_signup_PUT_w_user(self):
        """
        Test signup view with user logged in using PUT method.
        Should return method not allowed.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.put(reverse('todo_list_app:signup'))
        self.assertEquals(response.status_code, 405)



    def test_signup_DELETE_wo_user(self):
        """
        Test signup view without user logged in using DELETE method.
        Should return method not allowed.
        """
        response = self.client.delete(reverse('todo_list_app:signup'))
        self.assertEquals(response.status_code, 405)



    def test_signup_DELETE_w_user(self):
        """
        Test signup view with user logged in using DELETE method.
        Should return method not allowed.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.delete(reverse('todo_list_app:signup'))
        self.assertEquals(response.status_code, 405)
