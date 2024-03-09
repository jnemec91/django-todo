from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from todo_list_app.models import UserOptions, TodoList, TodoField
from .setup import TestSetup

class TestListDetailsView(TestCase):
    """
    Class for testing of detail view of todo list application.
    """
    
    def setUp(self) -> None:
        """
        Method for setting up test environment.
        """
        self.setup = TestSetup()
        self.client = self.setup.client
        self.user = self.setup.user

        self.todo_list = TodoList.objects.create(name='test_list', created_by=self.user, access_granted=False)
        self.todo_list.owner.add(self.user)
        self.todo_list.hash = self.todo_list._create_hash()
        self.list_hash = self.todo_list.hash
        self.todo_list.save()
    


    def test_list_details_GET_wo_user(self):
        """
        Test list details view without user logged in and with data using GET method.
        Should return list details page with todo list as dictionary in context.
        """
        response = self.client.get(reverse('todo_list_app:list_details', kwargs={'todo_list_hash': self.list_hash}))
        self.assertEqual(response.status_code, 200)

        for template in ('todo_list/detail.html',
                         'todo_list/base.html',
                         'todo_list/navbar.html',
                         'todo_list/footer.html'
                         ):
            self.assertTemplateUsed(response, template)

        self.assertIn('todo_lists', response.context)
        self.assertEqual(response.context['todo_lists'], [{'id':1,
                                                             'name': 'test_list',
                                                             'created_by': self.user,
                                                             'owner': [self.user],
                                                             'fields': [],
                                                             'hash': self.list_hash,
                                                             'access_granted': False,
                                                             }])



    def test_list_details_GET_w_user(self):
        """
        Test list details view with user logged in and with data using GET method.
        Should return list details page with todo list as dictionary in context.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('todo_list_app:list_details', kwargs={'todo_list_hash': self.list_hash}))
        self.assertEqual(response.status_code, 200)

        for template in ('todo_list/detail.html',
                         'todo_list/base.html',
                         'todo_list/navbar.html',
                         'todo_list/footer.html'
                         ):
            self.assertTemplateUsed(response, template)

        self.assertIn('todo_lists', response.context)
        self.assertEqual(response.context['todo_lists'], [{'id':1,
                                                         'name': 'test_list',
                                                         'created_by': self.user,
                                                         'owner': [self.user],
                                                         'fields': [],
                                                         'hash': self.list_hash,
                                                         'access_granted': False,
                                                         }])
    


    def test_list_details_POST_wo_user(self):
        """
        Test list details view without user logged in and with data using POST method.
        Should redirect return error 405.
        """
        response = self.client.post(reverse('todo_list_app:list_details', kwargs={'todo_list_hash': self.list_hash}))
        self.assertEqual(response.status_code, 405)



    def test_list_details_POST_w_user(self):
        """
        Test list details view with user logged in and with data using POST method.
        Should redirect return error 405.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('todo_list_app:list_details', kwargs={'todo_list_hash': self.list_hash}))
        self.assertEqual(response.status_code, 405)



    def test_list_details_PUT_wo_user(self):
        """
        Test list details view without user logged in and with data using PUT method.
        Should redirect return error 405.
        """
        response = self.client.put(reverse('todo_list_app:list_details', kwargs={'todo_list_hash': self.list_hash}))
        self.assertEqual(response.status_code, 405)
    


    def test_list_details_PUT_w_user(self):
        """
        Test list details view with user logged in and with data using PUT method.
        Should redirect return error 405.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.put(reverse('todo_list_app:list_details', kwargs={'todo_list_hash': self.list_hash}))
        self.assertEqual(response.status_code, 405)
    


    def test_list_details_DELETE_wo_user(self):
        """
        Test list details view without user logged in and with data using DELETE method.
        Should redirect return error 405.
        """
        response = self.client.delete(reverse('todo_list_app:list_details', kwargs={'todo_list_hash': self.list_hash}))
        self.assertEqual(response.status_code, 405)



    def test_list_details_DELETE_w_user(self):
        """
        Test list details view with user logged in and with data using DELETE method.
        Should redirect return error 405.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.delete(reverse('todo_list_app:list_details', kwargs={'todo_list_hash': self.list_hash}))
        self.assertEqual(response.status_code, 405)
    