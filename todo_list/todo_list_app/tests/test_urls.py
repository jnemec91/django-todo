from django.test import SimpleTestCase
from django.urls import reverse, resolve
from todo_list_app.views import *

class TestUrls(SimpleTestCase):
    """
    This class tests if urls are resolved to correct views.
    """

    def test_url_index_resolves(self):
        url = reverse('todo_list_app:index')
        self.assertEqual(resolve(url).func, index)
    
    def test_url_login_resolves(self):
        url = reverse('todo_list_app:login')
        self.assertEqual(resolve(url).func, user_login)
    
    def test_url_signup_resolves(self):
        url = reverse('todo_list_app:signup')
        self.assertEqual(resolve(url).func, signup)
    
    def test_url_logout_resolves(self):
        url = reverse('todo_list_app:logout')
        self.assertEqual(resolve(url).func, log_out)
    
    def test_url_create_todo_list_resolves(self):
        url = reverse('todo_list_app:create_todo_list')
        self.assertEqual(resolve(url).func, create_todo_list)
    
    def test_url_edit_todo_list_resolves(self):
        url = reverse('todo_list_app:edit_todo_list', args=['hash'])
        self.assertEqual(resolve(url).func, edit_todo_list)
    
    def test_url_delete_todo_list_resolves(self):
        url = reverse('todo_list_app:delete_todo_list', args=['hash'])
        self.assertEqual(resolve(url).func, delete_todo_list)
    
    def test_url_list_of_todo_lists_resolves(self):
        url = reverse('todo_list_app:list_of_todo_lists')
        self.assertEqual(resolve(url).func, list_of_todo_lists)
    
    def test_url_list_details_resolves(self):
        url = reverse('todo_list_app:list_details', args=['hash'])
        self.assertEqual(resolve(url).func, list_details)
    
    def test_url_check_task_resolves(self):
        url = reverse('todo_list_app:check_task', args=[1])
        self.assertEqual(resolve(url).func, check_task)
    
    def test_url_settings_resolves(self):
        url = reverse('todo_list_app:settings')
        self.assertEqual(resolve(url).func, settings)
    
    def test_url_add_to_my_list_resolves(self):
        url = reverse('todo_list_app:add_to_my_list', args=[1])
        self.assertEqual(resolve(url).func, add_to_my_list)
    
    def test_url_remove_from_shared_list_resolves(self):
        url = reverse('todo_list_app:remove_from_shared_list', args=[1, 1])
        self.assertEqual(resolve(url).func, remove_from_shared_list)
    
    def test_url_password_reset_resolves(self):
        url = reverse('todo_list_app:password_reset')
        self.assertEqual(resolve(url).func.view_class, ToDoAppPasswordResetView)
    
    def test_url_password_reset_done_resolves(self):
        url = reverse('todo_list_app:password_reset_done')
        self.assertEqual(resolve(url).func.view_class, ToDoAppPasswordResetDoneView)
    
    def test_url_password_reset_confirm_resolves(self):
        url = reverse('todo_list_app:password_reset_confirm', args=['uidb64', 'token'])
        self.assertEqual(resolve(url).func.view_class, ToDoAppPasswordResetConfirmView)
    
    def test_url_password_reset_complete_resolves(self):
        url = reverse('todo_list_app:password_reset_complete')
        self.assertEqual(resolve(url).func.view_class, ToDoAppPasswordResetCompleteView)
    