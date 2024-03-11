from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from todo_list_app.models import UserOptions, TodoList, TodoField
from .setup import TestSetup
from datetime import date

class TestDeleteView(TestCase):
    """
    Class for testing delete todo list view of todo list application.
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

        # create another users todo list
        self.another_todo_list = TodoList.objects.create(name='another_list',
                                            created_by=self.another_user,
                                            access_granted=False)
        self.another_todo_list.owner.add(self.another_user)
        self.another_todo_list.owner.add(self.user)
        self.another_todo_list.hash = self.another_todo_list._create_hash()
        self.another_todo_list.save()


    def test_delete_GET_wo_user(self):
        """
        Test delete view without user logged in and with data using GET method.
        Should redirect to login page.
        """
        response = self.client.get(reverse('todo_list_app:delete_todo_list', args=[self.user_todo_list.id]))
        self.assertRedirects(response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:delete_todo_list', args=[self.user_todo_list.id]) }", status_code=302)
    


    def test_delete_GET_w_user(self):
        """
        Test delete view with user logged in and with data using GET method.
        Should return status 405.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.get(reverse('todo_list_app:delete_todo_list', args=[self.user_todo_list.id]))
        self.assertEqual(self.response.status_code, 405)


    
    def test_delete_POST_wo_user(self):
        """
        Test delete view without user logged in and with data using POST method.
        Should redirect to login page.
        """
        self.response = self.client.post(reverse('todo_list_app:delete_todo_list', args=[self.user_todo_list.id]))
        self.assertRedirects(self.response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:delete_todo_list', args=[self.user_todo_list.id]) }", status_code=302)



    def test_delete_POST_w_user(self):
        """
        Test delete view with user logged in and with data using POST method.
        Should delete todo list and redirect to index page.
        """
        self.assertEqual(TodoList.objects.filter(owner=self.user).count(), 2)
        self.client.login(username='testuser', password='12345')
        self.response = self.client.post(reverse('todo_list_app:delete_todo_list', args=[self.user_todo_list.id]),HTTP_REFERER=reverse('todo_list_app:index'))
        self.assertEqual(TodoList.objects.count(), 1)
        self.assertEqual(TodoList.objects.filter(id=self.user_todo_list.id).exists(), False)
        self.assertRedirects(self.response, reverse('todo_list_app:index'), status_code=302)        


    def test_delete_POST_w_user_another_user(self):
        """
        Test delete view with user logged in and with data using POST method.
        Should delete todo list and redirect to index page.
        """
        self.assertEqual(TodoList.objects.filter(owner=self.user).count(), 2)
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('todo_list_app:delete_todo_list', args=[self.another_todo_list.id]),HTTP_REFERER=reverse('todo_list_app:index'))
        self.assertEqual(TodoList.objects.count(), 2)
        self.assertEqual(TodoList.objects.filter(owner=self.user).count(), 1)
        self.assertEqual(TodoList.objects.filter(created_by=self.another_user).count(), 1)
        self.assertRedirects(response, reverse('todo_list_app:index'), status_code=302)

    

    def test_delete_POST_w_user_invalid_id(self):
        """
        Test delete view with user logged in and with invalid data using POST method.
        Should return redirect to index page.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.post(reverse('todo_list_app:delete_todo_list', args=[100]),HTTP_REFERER=reverse('todo_list_app:index'))
        self.assertEqual(self.response.status_code, 404)

    

    def test_delete_PUT_wo_user(self):
        """
        Test delete view without user logged in and with data using PUT method.
        Should redirect to login page.
        """
        response = self.client.put(reverse('todo_list_app:delete_todo_list', args=[self.user_todo_list.id]))
        self.assertRedirects(response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:delete_todo_list', args=[self.user_todo_list.id]) }", status_code=302)



    def test_delete_PUT_w_user(self):
        """
        Test delete view with user logged in and with data using PUT method.
        Should return status 405.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.put(reverse('todo_list_app:delete_todo_list', args=[self.user_todo_list.id]))
        self.assertEqual(self.response.status_code, 405)



    def test_delete_DELETE_wo_user(self):
        """
        Test delete view without user logged in and with data using DELETE method.
        Should redirect to login page.
        """
        self.response = self.client.delete(reverse('todo_list_app:delete_todo_list', args=[self.user_todo_list.id]))
        self.assertRedirects(self.response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:delete_todo_list', args=[self.user_todo_list.id]) }", status_code=302)


    
    def test_delete_DELETE_w_user(self):
        """
        Test delete view with user logged in and with data using PUT method.
        Should return status 405.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.put(reverse('todo_list_app:delete_todo_list', args=[self.user_todo_list.id]))
        self.assertEqual(self.response.status_code, 405)