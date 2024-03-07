from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from todo_list_app.models import UserOptions, TodoList, TodoField
from .setup import TestSetup

class TestIndexView(TestCase):
    """
    Class for testing index view of todo list application.
    """
    
    def setUp(self) -> None:
        """
        Method for setting up test environment.
        """
        self.setup = TestSetup()
        self.client = self.setup.client
        self.user = self.setup.user
        self.another_user = self.setup.another_user

    
    def test_index_GET_wo_user(self):
        """
        Test index view without user logged in and without data using GET method.
        Should redirect to login page.
        """
        response = self.client.get(reverse('todo_list_app:index'))
        self.assertRedirects(response, reverse('todo_list_app:login'), status_code=302)

    
    def test_index_GET_w_user(self):
        """
        Test index view with user logged in and without data using GET method.
        Should return index page with user's todo lists as list of dictionaries in context.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('todo_list_app:index'))
        self.assertEquals(response.status_code, 200)
        for template in ('todo_list/index.html',
                         'todo_list/base.html',
                         'todo_list/navbar.html',
                         'todo_list/footer.html'
                         ):
            self.assertTemplateUsed(response, template)
        self.assertIn('todo_lists', response.context)
        self.assertEquals(response.context['todo_lists'], [])


    def test_index_POST_wo_user(self):
        """
        Test index view with POST request without user logged in and without data.
        Should redirect return error 405.
        """
        response = self.client.post(reverse('todo_list_app:index'))
        self.assertEquals(response.status_code, 405)


    def test_index_POST_w_user(self):
        """
        Test index view with POST request with user logged in and without data.
        Should redirect return error 405.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('todo_list_app:index'))
        self.assertEquals(response.status_code, 405)


    def test_index_PUT_wo_user(self):
        """
        Test index view with PUT request without user logged in and without data.
        Should redirect return error 405.
        """
        response = self.client.put(reverse('todo_list_app:index'))
        self.assertEquals(response.status_code, 405)


    def test_index_PUT_w_user(self):
        """
        Test index view with PUT request with user logged in and without data.
        Should redirect return error 405.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.put(reverse('todo_list_app:index'))
        self.assertEquals(response.status_code, 405)



    def test_index_DELETE_wo_user(self):
        """
        Test index view with DELETE request without user logged in and without data.
        Should redirect return error 405.
        """
        response = self.client.delete(reverse('todo_list_app:index'))
        self.assertEquals(response.status_code, 405)
    

    def test_index_DELETE_w_user(self):
        """
        Test index view with DELETE request with user logged in and without data.
        Should redirect return error 405.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.delete(reverse('todo_list_app:index'))
        self.assertEquals(response.status_code, 405)

    # test index view with user logged in and with data using GET method
    def test_index_GET_w_user_w_data(self):
        """
        Test index view with user logged in and with data using GET method.
        Should return index page with todo list as dictionary in context.
        """
        self.client.login(username='testuser', password='12345')

        # create todo list
        todo_list = TodoList.objects.create(name='test_list', created_by=self.user, access_granted=False)
        todo_list.owner.add(self.user)
        todo_list.hash = todo_list._create_hash()
        list_hash = todo_list.hash
        todo_list.save()

        # create todo list
        todo_list = TodoList.objects.create(name='another_test_list', created_by=self.another_user, access_granted=False)
        todo_list.owner.add(self.another_user)
        todo_list.hash = todo_list._create_hash()
        list_hash = todo_list.hash
        todo_list.save()

        response = self.client.get(reverse('todo_list_app:index'))
        self.assertEquals(response.status_code, 200)

        for template in ('todo_list/index.html',
                         'todo_list/base.html',
                         'todo_list/navbar.html',
                         'todo_list/footer.html'
                         ):
            self.assertTemplateUsed(response, template)

        self.assertIn('todo_lists', response.context)
        self.assertEquals(response.context['todo_lists'], [{'id':1,
                                                             'name': 'test_list',
                                                             'created_by': self.user,
                                                             'owner': [self.user],
                                                             'fields': [],
                                                             'hash': list_hash,
                                                             }])

    # test index view with user logged in and with data using POST method
    def test_index_POST_w_user_w_data(self):
        """
        Test index view with user logged in and with data using POST method.
        Should redirect return error 405.
        """
        self.client.login(username='testuser', password='12345')

        # create todo list
        todo_list = TodoList.objects.create(name='test_list', created_by=self.user, access_granted=False)
        todo_list.owner.add(self.user)
        todo_list.hash = todo_list._create_hash()
        list_hash = todo_list.hash
        todo_list.save()

        response = self.client.post(reverse('todo_list_app:index'))
        self.assertEquals(response.status_code, 405)
    
    # test index view with user logged in and with data using PUT method
    def test_index_PUT_w_user_w_data(self):
        """
        Test index view with user logged in and with data using PUT method.
        Should redirect return error 405.
        """
        self.client.login(username='testuser', password='12345')

        # create todo list
        todo_list = TodoList.objects.create(name='test_list', created_by=self.user, access_granted=False)
        todo_list.owner.add(self.user)
        todo_list.hash = todo_list._create_hash()
        list_hash = todo_list.hash
        todo_list.save()

        response = self.client.put(reverse('todo_list_app:index'))
        self.assertEquals(response.status_code, 405)
    
    # test index view with user logged in and with data using DELETE method
    def test_index_DELETE_w_user_w_data(self):
        """
        Test index view with user logged in and with data using DELETE method.
        Should redirect return error 405.
        """
        self.client.login(username='testuser', password='12345')

        # create todo list
        todo_list = TodoList.objects.create(name='test_list', created_by=self.user, access_granted=False)
        todo_list.owner.add(self.user)
        todo_list.hash = todo_list._create_hash()
        list_hash = todo_list.hash
        todo_list.save()

        response = self.client.delete(reverse('todo_list_app:index'))
        self.assertEquals(response.status_code, 405)