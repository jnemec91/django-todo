from datetime import date
from django.urls import reverse
from django.test import TestCase

from todo_list_app.models import TodoList, TodoField
from .setup import TestSetup



class TestAddToMyListkView(TestCase):
    """
    Class for testing add to my list view of todo list application.
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
                                                   text='text',
                                                   created_at=date.today(),
                                                   deadline_at=date.today(),
                                                   checked=False)

        self.user_todo_list.fields.add(self.todo_field)
        self.user_todo_list.save()

        # create another users todo list
        self.another_todo_list = TodoList.objects.create(name='another_list',
                                                         created_by=self.another_user,
                                                         access_granted=False)
        self.another_todo_list.owner.add(self.another_user)
        self.another_todo_list.hash = self.another_todo_list._create_hash()
        self.another_todo_list.save()

        self.another_todo_field = TodoField.objects.create(name='todo field',
                                                           text='text',
                                                           created_at=date.today(),
                                                           deadline_at=date.today(),
                                                           checked=False)

        self.another_todo_list.fields.add(self.another_todo_field)
        self.another_todo_list.save()

    def test_add_to_my_list_get_wo_user(self):
        """
        Test for get request to add to my list view without user logged in.
        Should redirect to login page.
        """

        self.response = self.client.get(
            reverse('todo_list_app:add_to_my_list', args=[self.user_todo_list.hash]))
        self.assertRedirects(
            self.response,
            f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:add_to_my_list',args=[self.user_todo_list.hash]) }", status_code=302)

    def test_add_to_my_list_get_w_user(self):
        """
        Test for get request to add to my list view with user logged in.
        Should return status 405.
        """

        self.client.login(username='testuser', password='12345')
        self.response = self.client.get(
            reverse('todo_list_app:add_to_my_list', args=[self.user_todo_list.hash]))
        self.assertEqual(self.response.status_code, 405)

    def test_add_to_my_list_post_wo_user(self):
        """
        Test for post request to add to my list view without user logged in.
        Should redirect to login page.
        """

        self.response = self.client.post(
            reverse('todo_list_app:add_to_my_list', args=[self.user_todo_list.hash]))
        self.assertRedirects(
            self.response,
            f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:add_to_my_list', args=[self.user_todo_list.hash]) }", status_code=302)

    def test_add_to_my_list_post_w_user(self):
        """
        Test for post request to add to my list view with user logged in with list that user dont own.
        Should return response 200 with content 'reload'
        """

        self.client.login(username='testuser', password='12345')
        self.response = self.client.post(
            reverse('todo_list_app:add_to_my_list', args=[self.another_todo_list.hash]))
        self.assertTrue(TodoList.objects.filter(
            hash=self.another_todo_list.hash).filter(owner=self.user.id).exists())
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.content, b'reload')

    def test_add_to_my_list_post_w_user_own_list(self):
        """
        Test for post request to add to my list view with user logged in with list that user own.
        Should return response 200 with content 'reload'
        """

        self.client.login(username='testuser', password='12345')
        self.response = self.client.post(
            reverse('todo_list_app:add_to_my_list', args=[self.user_todo_list.hash]))
        self.assertTrue(TodoList.objects.filter(
            hash=self.user_todo_list.hash).filter(owner=self.user.id).exists())
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.content, b'reload')

    def test_add_to_my_list_post_w_user_invalid_id(self):
        """
        Test for post request to add to my list view with user logged in with invalid id.
        Should return status code 404.
        """

        self.client.login(username='testuser', password='12345')
        self.response = self.client.post(
            reverse('todo_list_app:add_to_my_list', args=[100]))
        self.assertEqual(self.response.status_code, 404)

    def test_add_to_my_list_put_wo_user(self):
        """
        Test for put request to add to my list view without user logged in.
        Should redirect to login page.
        """

        self.response = self.client.put(
            reverse('todo_list_app:add_to_my_list', args=[self.user_todo_list.hash]))
        self.assertRedirects(
            self.response,
            f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:add_to_my_list', args=[self.user_todo_list.hash]) }", status_code=302)

    def test_add_to_my_list_put_w_user(self):
        """
        Test for put request to add to my list view with user logged in.
        Should return status 405.
        """

        self.client.login(username='testuser', password='12345')
        self.response = self.client.put(
            reverse('todo_list_app:add_to_my_list', args=[self.user_todo_list.hash]))
        self.assertEqual(self.response.status_code, 405)

    def test_add_to_my_list_delete_wo_user(self):
        """
        Test for delete request to add to my list view without user logged in.
        Should redirect to login page.
        """

        self.response = self.client.delete(
            reverse('todo_list_app:add_to_my_list', args=[self.user_todo_list.hash]))
        self.assertRedirects(
            self.response,
            f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:add_to_my_list', args=[self.user_todo_list.hash]) }", status_code=302)

    def test_add_to_my_list_delete_w_user(self):
        """
        Test for delete request to add to my list view with user logged in.
        Should return status 405.
        """

        self.client.login(username='testuser', password='12345')
        self.response = self.client.delete(
            reverse('todo_list_app:add_to_my_list', args=[self.user_todo_list.hash]))
        self.assertEqual(self.response.status_code, 405)
