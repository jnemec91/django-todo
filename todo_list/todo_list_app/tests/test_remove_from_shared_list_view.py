from datetime import date
from django.urls import reverse
from django.test import TestCase

from todo_list_app.models import TodoList, TodoField
from .setup import TestSetup



class TestRemoveFromSharedListView(TestCase):
    """
    Class for testing remove from shared list view of todo list application.
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
        self.another_todo_list.owner.add(self.user)
        self.another_todo_list.hash = self.another_todo_list._create_hash()
        self.another_todo_list.save()

        self.another_todo_field = TodoField.objects.create(name='todo field',
                                                           text='text',
                                                           created_at=date.today(),
                                                           deadline_at=date.today(),
                                                           checked=False)

        self.another_todo_list.fields.add(self.another_todo_field)
        self.another_todo_list.save()



    def test_remove_from_shared_list_get_wo_user(self):
        """
        Test for GET request to remove from shared list view with user logged in.
        """

        response = self.client.get(reverse('todo_list_app:remove_from_shared_list', args=[self.another_todo_list.id, self.user.id]))
        self.assertRedirects(
            response,
            f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:remove_from_shared_list', args=[self.another_todo_list.id, self.user.id]) }",
            status_code=302)



    def test_remove_from_shared_list_get_with_user(self):
        """
        Test for GET request to remove from shared list view with user logged in.
        """

        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('todo_list_app:remove_from_shared_list', args=[self.another_todo_list.id, self.user.id]))
        self.assertEqual(response.status_code, 405)



    def test_remove_from_shared_list_post_wo_user(self):
        """
        Test for POST request to remove from shared list view with user not logged in.
        """

        response = self.client.post(reverse('todo_list_app:remove_from_shared_list', args=[self.another_todo_list.id, self.user.id]))
        self.assertRedirects(
            response,
            f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:remove_from_shared_list', args=[self.another_todo_list.id, self.user.id]) }",
            status_code=302)



    def test_remove_from_shared_list_post_with_user(self):
        """
        Test for POST request to remove from shared list view with user logged in.
        """

        self.client.login(username='anotheruser', password='12345')
        self.assertEqual(self.another_todo_list.owner.count(), 2)
        response = self.client.post(reverse('todo_list_app:remove_from_shared_list', args=[self.another_todo_list.id, self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'reload')
        self.assertFalse(self.another_todo_list.owner.filter(id=self.user.id).exists())
        self.assertEqual(self.another_todo_list.owner.count(), 1)



    def test_remove_from_shared_list_post_with_user_own_list(self):
        """
        Test for POST request to remove from shared list view with user logged in with list that user own.
        """

        self.client.login(username='testuser', password='12345')
        self.assertEqual(self.user_todo_list.owner.count(), 1)
        response = self.client.post(reverse('todo_list_app:remove_from_shared_list', args=[self.user_todo_list.id, self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'reload')
        self.assertEqual(self.user_todo_list.owner.count(), 1)
        self.assertTrue(self.user_todo_list.owner.filter(id=self.user.id).exists())



    def test_remove_from_shared_list_post_with_user_not_in_list(self):
        """
        Test for POST request to remove from shared list view with user logged in with list that user is not in.
        """

        self.client.login(username='testuser', password='12345')
        self.assertEqual(self.user_todo_list.owner.count(), 1)
        response = self.client.post(reverse('todo_list_app:remove_from_shared_list', args=[self.user_todo_list.id, self.another_user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'reload')
        self.assertEqual(self.user_todo_list.owner.count(), 1)



    def test_remove_from_shared_list_post_with_user_invalid_id(self):
        """
        Test for POST request to remove from shared list view with user logged in with invalid id.
        """

        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('todo_list_app:remove_from_shared_list', args=[self.another_todo_list.id, 999]))
        self.assertEqual(response.status_code, 404)



    def test_remove_from_shared_list_post_with_user_invalid_list_id(self):
        """
        Test for POST request to remove from shared list view with user logged in with invalid list id.
        """

        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('todo_list_app:remove_from_shared_list', args=[999, self.user.id]))
        self.assertEqual(response.status_code, 404)



    def test_remove_from_shared_list_put_wo_user(self):
        """
        Test for PUT request to remove from shared list view without user logged in.
        """

        response = self.client.put(reverse('todo_list_app:remove_from_shared_list', args=[self.another_todo_list.id, self.user.id]))
        self.assertRedirects(
            response,
            f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:remove_from_shared_list', args=[self.another_todo_list.id, self.user.id]) }",
            status_code=302)



    def test_remove_from_shared_list_put_with_user(self):
        """
        Test for PUT request to remove from shared list view with user logged in.
        """

        self.client.login(username='anotheruser', password='12345')
        self.assertEqual(self.another_todo_list.owner.count(), 2)
        response = self.client.put(reverse('todo_list_app:remove_from_shared_list', args=[self.another_todo_list.id, self.user.id]))
        self.assertEqual(response.status_code, 405)



    def test_remove_from_shared_list_delete_wo_user(self):
        """
        Test for DELETE request to remove from shared list view without user logged in.
        """

        response = self.client.delete(reverse('todo_list_app:remove_from_shared_list', args=[self.another_todo_list.id, self.user.id]))
        self.assertRedirects(
            response,
            f"{ reverse('todo_list_app:login') }?next={ reverse('todo_list_app:remove_from_shared_list', args=[self.another_todo_list.id, self.user.id]) }",
            status_code=302)



    def test_remove_from_shared_list_delete_with_user(self):
        """
        Test for DELETE request to remove from shared list view with user logged in.
        """

        self.client.login(username='anotheruser', password='12345')
        self.assertEqual(self.another_todo_list.owner.count(), 2)
        response = self.client.delete(reverse('todo_list_app:remove_from_shared_list', args=[self.another_todo_list.id, self.user.id]))
        self.assertEqual(response.status_code, 405)
