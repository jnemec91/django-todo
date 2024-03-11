from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from todo_list_app.models import UserOptions, TodoList, TodoField
from .setup import TestSetup
from datetime import date

class TestEditTodoListView(TestCase):
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

        # create another users todo list
        self.another_todo_list = TodoList.objects.create(name='another_list',
                                            created_by=self.another_user,
                                            access_granted=False)
        self.another_todo_list.owner.add(self.another_user)
        self.another_todo_list.owner.add(self.user)
        self.another_todo_list.hash = self.another_todo_list._create_hash()
        self.another_todo_list.save()



    def test_edit_GET_wo_user(self):
        """
        Test edit view without user logged in and with data using GET method.
        Should redirect to login page.
        """
        response = self.client.get(reverse('todo_list_app:edit_todo_list', args=[self.user_todo_list.id]))
        self.assertRedirects(response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:edit_todo_list', args=[self.user_todo_list.id]) }", status_code=302)
    
    

    def test_edit_GET_w_user(self):
        """
        Test edit view with user logged in and with data using GET method.
        Should return status 405.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.get(reverse('todo_list_app:edit_todo_list', args=[self.user_todo_list.id]))
        self.assertEqual(self.response.status_code, 200)
        for template in ('todo_list/create_todo_list.html',
                         'todo_list/base.html',
                         'todo_list/navbar.html',
                         'todo_list/footer.html'
                         ):
            self.assertTemplateUsed(self.response, template)
        self.assertIn('todo_list', self.response.context)
        self.assertIn('todo_fields', self.response.context)
        self.assertEqual(self.response.context['todo_list'], self.user_todo_list)



    def test_edit_GET_w_user_invalid_id(self):
        """
        Test edit view with user logged in and with invalid data using GET method.
        Should return status 404.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.get(reverse('todo_list_app:edit_todo_list', args=[100]))
        self.assertEqual(self.response.status_code, 404)    

    def test_edit_POST_wo_user(self):
        """
        Test edit view without user logged in and with data using POST method.
        Should redirect to login page.
        """
        self.response = self.client.post(reverse('todo_list_app:edit_todo_list', args=[self.user_todo_list.id]))
        self.assertRedirects(self.response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:edit_todo_list', args=[self.user_todo_list.id]) }", status_code=302)

    

    def test_edit_POST_w_user(self):
        """
        Test edit view with user logged in and with data using POST method.
        Should update todo list and redirect to index page.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.post(reverse('todo_list_app:edit_todo_list',
                                                 args=[self.user_todo_list.id]),
                                                 data={'name': 'new name',
                                                       'is-shared': '1',
                                                       'fields_new': ['new field'],
                                                       'descriptions_new': ['new description'],
                                                       'deadlines_new': [date.today()],
                                                       })
        self.assertRedirects(self.response, reverse('todo_list_app:index'), status_code=302)
        self.user_todo_list.refresh_from_db()
        self.assertEqual(self.user_todo_list.name, 'new name')
        self.assertEqual(self.user_todo_list.access_granted, True)
        self.assertEqual(self.user_todo_list.fields.count(), 1)
        self.assertEqual(self.user_todo_list.fields.first().name, 'new field')
        self.assertEqual(self.user_todo_list.fields.first().text, 'new description')
        self.assertEqual(self.user_todo_list.fields.first().deadline_at, date.today())
        self.assertEqual(self.user_todo_list.owner.count(), 1)
        self.assertEqual(self.user_todo_list.owner.first(), self.user)
        self.assertEqual(self.user_todo_list.created_by, self.user)



    def test_edit_POST_w_user_another_users_list(self):
        """
        Test edit view with user logged in and with data using POST method.
        Should update todo list and redirect to index page.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.post(reverse('todo_list_app:edit_todo_list',
                                                 args=[self.another_todo_list.id]),
                                                 data={'name': 'new name',
                                                       'is-shared': '1',
                                                       'fields_new': ['new field'],
                                                       'descriptions_new': ['new description'],
                                                       'deadlines_new': [date.today()],
                                                       })
        self.assertRedirects(self.response, reverse('todo_list_app:index'), status_code=302)
        self.another_todo_list.refresh_from_db()
        self.assertEqual(self.another_todo_list.name, 'new name')
        self.assertEqual(self.another_todo_list.access_granted, True)
        self.assertEqual(self.another_todo_list.fields.count(), 1)
        self.assertEqual(self.another_todo_list.fields.first().name, 'new field')
        self.assertEqual(self.another_todo_list.fields.first().text, 'new description')
        self.assertEqual(self.another_todo_list.fields.first().deadline_at, date.today())
        self.assertEqual(self.another_todo_list.owner.count(), 2)
        self.assertEqual(self.another_todo_list.created_by, self.another_user)



    def test_edit_POST_w_user_w_invalid_id(self):
        """
        Test edit view with user logged in and with invalid data using POST method.
        Should redirect to index page.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.post(reverse('todo_list_app:edit_todo_list',
                                                 args=[100]),
                                                 data={'name': 'new name',
                                                       'is-shared': '1',
                                                       'fields_new': ['new field'],
                                                       'descriptions_new': ['new description'],
                                                       'deadlines_new': [date.today()],
                                                       })
        self.assertEqual(self.response.status_code, 404)
        self.assertEqual(self.user_todo_list.name, 'todo list')
        self.assertEqual(self.user_todo_list.access_granted, False)
        self.assertEqual(self.user_todo_list.fields.count(), 0)
        self.assertEqual(self.user_todo_list.owner.count(), 1)
        self.assertEqual(self.user_todo_list.created_by, self.user)



    def test_edit_PUT_wo_user(self):
        """
        Test edit view without user logged in and with data using PUT method.
        Should redirect to login page.
        """
        response = self.client.put(reverse('todo_list_app:edit_todo_list', args=[self.user_todo_list.id]))
        self.assertRedirects(response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:edit_todo_list', args=[self.user_todo_list.id]) }", status_code=302)



    def test_edit_PUT_w_user(self):
        """
        Test edit view with user logged in and with data using PUT method.
        Should return status 405.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.put(reverse('todo_list_app:edit_todo_list', args=[self.user_todo_list.id]))
        self.assertEqual(self.response.status_code, 405)



    def test_edit_DELETE_wo_user(self):
        """
        Test edit view without user logged in and with data using DELETE method.
        Should redirect to login page.
        """
        response = self.client.delete(reverse('todo_list_app:edit_todo_list', args=[self.user_todo_list.id]))
        self.assertRedirects(response, f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:edit_todo_list', args=[self.user_todo_list.id]) }", status_code=302)



    def test_edit_DELETE_w_user(self):
        """
        Test edit view with user logged in and with data using DELETE method.
        Should return status 405.
        """
        self.client.login(username='testuser', password='12345')
        self.response = self.client.delete(reverse('todo_list_app:edit_todo_list', args=[self.user_todo_list.id]))
        self.assertEqual(self.response.status_code, 405)