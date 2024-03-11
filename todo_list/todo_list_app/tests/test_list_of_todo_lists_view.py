from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from todo_list_app.models import UserOptions, TodoList, TodoField
from .setup import TestSetup
from datetime import date

class TestListOfTodoListsView(TestCase):
    """
    Class for testing list of todo lists view of todo list application.
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



    def test_list_GET_wo_user(self):
        """
        Test list view without user logged in using GET method.
        Should redirect to login page.
        """
        response = self.client.get(reverse('todo_list_app:list_of_todo_lists'))
        self.assertRedirects(response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:list_of_todo_lists') }", status_code=302)



    def test_list_GET_w_user(self):
        """
        Test list view with user logged in using GET method.
        Should return status 200.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.get(reverse('todo_list_app:list_of_todo_lists'))
        self.assertEqual(self.response.status_code, 200)
        for template in ('todo_list/list_of_todo_lists.html',
                         'todo_list/base.html',
                         'todo_list/navbar.html',
                         'todo_list/footer.html'
                         ):
            self.assertTemplateUsed(self.response, template)
        self.assertIn('todo_lists', self.response.context)
        self.assertEqual(len(self.response.context['todo_lists']), 2)



    def test_list_POST_wo_user(self):
        """
        Test list view without user logged in using POST method.
        Should redirect to login page.
        """
        self.response = self.client.post(reverse('todo_list_app:list_of_todo_lists'))
        self.assertRedirects(self.response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:list_of_todo_lists') }", status_code=302)



    def test_list_POST_w_user(self):
        """
        Test list view with user logged in using POST method.
        Should return status 405.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.post(reverse('todo_list_app:list_of_todo_lists'))
        self.assertEqual(self.response.status_code, 405)



    def test_list_of_todo_lists_PUT_wo_user(self):
        """
        Test list view without user logged in using PUT method.
        Should redirect to login page.
        """
        self.response = self.client.put(reverse('todo_list_app:list_of_todo_lists'))
        self.assertRedirects(self.response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:list_of_todo_lists') }", status_code=302)



    def test_list_of_todo_lists_PUT_w_user(self):
        """
        Test list view with user logged in using PUT method.
        Should return status 405.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.put(reverse('todo_list_app:list_of_todo_lists'))
        self.assertEqual(self.response.status_code, 405)



    def test_list_of_todo_lists_DELETE_wo_user(self):
        """
        Test list view without user logged in using DELETE method.
        Should redirect to login page.
        """
        self.response = self.client.delete(reverse('todo_list_app:list_of_todo_lists'))
        self.assertRedirects(self.response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:list_of_todo_lists') }", status_code=302)