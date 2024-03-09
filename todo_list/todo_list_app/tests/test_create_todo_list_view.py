from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from todo_list_app.models import UserOptions, TodoList, TodoField
from .setup import TestSetup
from datetime import date

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



    def test_create_todo_list_GET_wo_user_logged_in(self):
        """
        Test for GET request to create todo list view without user logged in.
        Should redirect to login page.
        """

        response = self.client.get(reverse('todo_list_app:create_todo_list'))
        self.assertRedirects(response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:create_todo_list') }", status_code=302)



    def test_create_todo_list_GET_with_user_logged_in(self):
        """
        Test for GET request to create todo list view with user logged in.
        Should return create todo list page.
        """

        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('todo_list_app:create_todo_list'))
        self.assertEqual(response.status_code, 200)
        for template in ('todo_list/create_todo_list.html',
                         'todo_list/base.html',
                         'todo_list/navbar.html',
                         'todo_list/footer.html'
                         ):
            self.assertTemplateUsed(response, template)
        self.assertIn('new', response.context)
        self.assertEqual(response.context['new'], True)

    

    def test_create_todo_list_POST_wo_user_logged_in(self):
        """
        Test for POST request to create todo list view without user logged in.
        Should redirect to login page.
        """

        response = self.client.post(reverse('todo_list_app:create_todo_list'), data={'name': 'Test title',
                                                                                     'fields_new':['Test field'],
                                                                                     'descriptions_new': ['Test description'],
                                                                                     'deadlines_new': ['2021-12-31'],
                                                                                     'is-shared': '1',
                                                                                     })
        self.assertRedirects(response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:create_todo_list') }", status_code=302)
        self.assertFalse(TodoList.objects.filter(name='Test title').exists())



    def test_create_todo_list_POST_with_user_logged_in(self):
        """
        Test for POST request to create todo list view with user logged in.
        Should create todo list and redirect to index page.
        """

        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('todo_list_app:create_todo_list'), data={'name': 'Test title',
                                                                                     'fields_new':['Test field'],
                                                                                     'descriptions_new': ['Test description'],
                                                                                     'deadlines_new': ['2021-12-31'],
                                                                                     'is-shared': '1',
                                                                                     })
        
        self.assertRedirects(response, reverse('todo_list_app:index'), status_code=302)
        self.assertTrue(TodoList.objects.filter(name='Test title').exists())

        todo_list = TodoList.objects.get(name='Test title')

        self.assertEqual(todo_list.created_by, self.user)
        self.assertEqual(todo_list.owner.count(), 1)
        self.assertEqual(todo_list.owner.first(), self.user)
        self.assertEqual(todo_list.access_granted, True)
        self.assertEqual(todo_list.hash, todo_list._create_hash())
        self.assertEqual(todo_list.created_at.date(), date.today())

        self.assertEqual(todo_list.fields.count(), 1)
        self.assertEqual(todo_list.fields.first().name, 'Test field')
        self.assertEqual(todo_list.fields.first().text, 'Test description')
        self.assertEqual(todo_list.fields.first().checked, False)
        self.assertEqual(todo_list.fields.first().links_list, False) #this field is not used anywhere, it was added in preparation for future features
        self.assertEqual(todo_list.fields.first().list_link, None) #this field is not used anywhere, it was added in preparation for future features
        self.assertEqual(todo_list.fields.first().deadline_at, date(2021,12,31))
        


    def test_create_todo_list_PUT_wo_user_logged_in(self):
        """
        Test for PUT request to create todo list view without user logged in.
        Should redirect to login page.
        """

        response = self.client.put(reverse('todo_list_app:create_todo_list'), data={'name': 'Test title',
                                                                                    'fields_new':['Test field'],
                                                                                    'descriptions_new': ['Test description'],
                                                                                    'deadlines_new': ['2021-12-31'],
                                                                                    'is-shared': '1',
                                                                                    })
        self.assertRedirects(response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:create_todo_list') }", status_code=302)
        self.assertFalse(TodoList.objects.filter(name='Test title').exists())



    def test_create_todo_list_PUT_with_user_logged_in(self):
        """
        Test for PUT request to create todo list view with user logged in.
        Should return method not allowed response.
        """

        self.client.login(username='testuser', password='12345')
        response = self.client.put(reverse('todo_list_app:create_todo_list'), data={'name': 'Test title',
                                                                                    'fields_new':['Test field'],
                                                                                    'descriptions_new': ['Test description'],
                                                                                    'deadlines_new': ['2021-12-31'],
                                                                                    'is-shared': '1',
                                                                                    })
        self.assertEqual(response.status_code, 405)
        self.assertFalse(TodoList.objects.filter(name='Test title').exists())



    def test_create_todo_list_DELETE_wo_user_logged_in(self):
        """
        Test for DELETE request to create todo list view without user logged in.
        Should redirect to login page.
        """

        response = self.client.delete(reverse('todo_list_app:create_todo_list'), data={'name': 'Test title',
                                                                                       'fields_new':['Test field'],
                                                                                       'descriptions_new': ['Test description'],
                                                                                       'deadlines_new': ['2021-12-31'],
                                                                                       'is-shared': '1',
                                                                                       })
        self.assertRedirects(response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:create_todo_list') }", status_code=302)
        self.assertFalse(TodoList.objects.filter(name='Test title').exists())



    def test_create_todo_list_DELETE_with_user_logged_in(self):
        """
        Test for DELETE request to create todo list view with user logged in.
        Should return method not allowed response.
        """

        self.client.login(username='testuser', password='12345')
        response = self.client.delete(reverse('todo_list_app:create_todo_list'), data={'name': 'Test title',
                                                                                       'fields_new':['Test field'],
                                                                                       'descriptions_new': ['Test description'],
                                                                                       'deadlines_new': ['2021-12-31'],
                                                                                       'is-shared': '1',
                                                                                       })
        self.assertEqual(response.status_code, 405)
        self.assertFalse(TodoList.objects.filter(name='Test title').exists())