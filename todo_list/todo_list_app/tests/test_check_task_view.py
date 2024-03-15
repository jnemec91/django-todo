from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from todo_list_app.models import UserOptions, TodoList, TodoField
from .setup import TestSetup
from datetime import date

class TestCheckTaskView(TestCase):
    """
    Class for testing edit todo list view of todo list application.
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



    def test_check_task_GET_wo_user(self):
        """
        Test check task view without user logged in using GET method.
        Should redirect to login page.
        """
        response = self.client.get(reverse('todo_list_app:check_task', args=[1]))
        self.assertRedirects(response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:check_task', args=[1]) }", status_code=302)



    def test_check_task_GET_w_user(self):
        """
        Test check task view with user logged in using GET method.
        Should return status 405.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.get(reverse('todo_list_app:check_task', args=[1]))
        self.assertEqual(self.response.status_code, 405)



    def test_check_task_POST_wo_user(self):
        """
        Test check task view without user logged in using POST method.
        Should redirect to login page.
        """
        response = self.client.post(reverse('todo_list_app:check_task', args=[1]))
        self.assertRedirects(response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:check_task', args=[1]) }", status_code=302)



    def test_check_task_POST_w_user(self):
        """
        Test check task view with user logged in using POST method.
        Should return http response 'success'.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.post(reverse('todo_list_app:check_task', args=[1]))
        self.assertEqual(TodoField.objects.get(id=1).checked, True)
        self.assertEqual(self.response.content, b'success')



    def test_check_task_POST_w_user_invalid_id(self):
        """
        Test check task view with user logged in using POST method and invalid id.
        Should return status 404.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.post(reverse('todo_list_app:check_task', args=[100]))
        self.assertEqual(self.response.status_code, 404)



    def test_check_task_POST_w_user_another_user_not_shared(self):
        """
        Test check task view with user logged in using POST method but access not allowed.
        Should return status 403'
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.post(reverse('todo_list_app:check_task', args=[2]))
        self.assertEqual(TodoField.objects.get(id=2).checked, False)
        self.assertEqual(self.response.status_code, 403)        

    def test_check_task_POST_w_user_another_user_shared(self):
        """
        Test check task view with user logged in using POST method with allowed access.
        Should return http response 'success'.
        """
        todo_list = TodoList.objects.get(created_by=self.user)
        todo_list.access_granted = True
        todo_list.save()

        self.client.login(username='testuser', password='12345')
        self.response = self.client.post(reverse('todo_list_app:check_task', args=[2]))
        self.assertEqual(TodoField.objects.get(id=2).checked, False)
        self.assertEqual(self.response.status_code, 403)        


    def test_check_task_POST_w_another_user_user(self):
        """
        Test check task view with user logged in using POST method.
        Should return status code 403.
        """
        self.client.login(username='anotheruser', password='12345')
        self.response = self.client.post(reverse('todo_list_app:check_task', args=[1]))
        self.assertEqual(TodoField.objects.get(id=1).checked, False)
        self.assertEqual(self.response.status_code, 403)

    
    def test_check_task_PUT_wo_user(self):
        """
        Test check task view without user logged in using PUT method.
        Should return status 405.
        """
        response = self.client.put(reverse('todo_list_app:check_task', args=[1]))
        self.assertRedirects(response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:check_task', args=[1]) }", status_code=302)



    def test_check_task_PUT_w_user(self):
        """
        Test check task view with user logged in using PUT method.
        Should return status 405.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.put(reverse('todo_list_app:check_task', args=[1]))
        self.assertEqual(self.response.status_code, 405)



    def test_check_task_DELETE_wo_user(self):
        """
        Test check task view without user logged in using DELETE method.
        Should return status 405.
        """
        response = self.client.delete(reverse('todo_list_app:check_task', args=[1]))
        self.assertRedirects(response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:check_task', args=[1]) }", status_code=302)



    def test_check_task_DELETE_w_user(self):
        """
        Test check task view with user logged in using DELETE method.
        Should return status 405.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.delete(reverse('todo_list_app:check_task', args=[1]))
        self.assertEqual(self.response.status_code, 405)