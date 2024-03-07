from django.test import SimpleTestCase
from django.urls import reverse, resolve
from todo_list_app.views import *
from django.contrib.auth import views as auth_views

class TestUrls(SimpleTestCase):

    def test_url_index_resolves(self):
        url = reverse('todo_list_app:index')
        self.assertEquals(resolve(url).func, index)
    
    def test_url_login_resolves(self):
        url = reverse('todo_list_app:login')
        self.assertEquals(resolve(url).func, user_login)
    
    def test_url_signup_resolves(self):
        url = reverse('todo_list_app:signup')
        self.assertEquals(resolve(url).func, signup)
    
    def test_url_logout_resolves(self):
        url = reverse('todo_list_app:logout')
        self.assertEquals(resolve(url).func, log_out)
    
    def test_url_create_todo_list_resolves(self):
        url = reverse('todo_list_app:create_todo_list')
        self.assertEquals(resolve(url).func, create_todo_list)
    
    def test_url_edit_todo_list_resolves(self):
        url = reverse('todo_list_app:edit_todo_list', args=[1])
        self.assertEquals(resolve(url).func, edit_todo_list)
    
    def test_url_delete_todo_list_resolves(self):
        url = reverse('todo_list_app:delete_todo_list', args=[1])
        self.assertEquals(resolve(url).func, delete_todo_list)
    
    def test_url_list_of_todo_lists_resolves(self):
        url = reverse('todo_list_app:list_of_todo_lists')
        self.assertEquals(resolve(url).func, list_of_todo_lists)
    
    def test_url_list_details_resolves(self):
        url = reverse('todo_list_app:list_details', args=['hash'])
        self.assertEquals(resolve(url).func, list_details)
    
    def test_url_check_task_resolves(self):
        url = reverse('todo_list_app:check_task', args=[1])
        self.assertEquals(resolve(url).func, check_task)
    
    def test_url_settings_resolves(self):
        url = reverse('todo_list_app:settings')
        self.assertEquals(resolve(url).func, settings)
    
    def test_url_add_to_my_list_resolves(self):
        url = reverse('todo_list_app:add_to_my_list', args=[1])
        self.assertEquals(resolve(url).func, add_to_my_list)
    
    def test_url_remove_from_shared_list_resolves(self):
        url = reverse('todo_list_app:remove_from_shared_list', args=[1, 1])
        self.assertEquals(resolve(url).func, remove_from_shared_list)

    #TODO: Fix this tests
    
    # def test_url_password_reset_resolves(self):
    #     url = reverse('todo_list_app:password_reset')
    #     self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetView)
    
    # def test_url_password_reset_done_resolves(self):
    #     url = reverse('todo_list_app:password_reset_done')
    #     self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetDoneView)
    
    # def test_url_password_reset_confirm_resolves(self):
    #     url = reverse('todo_list_app:password_reset_confirm', args=['uidb64', 'token'])
    #     self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetConfirmView)
    
    # def test_url_password_reset_complete_resolves(self):
    #     url = reverse('todo_list_app:password_reset_complete')
    #     self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetCompleteView)
    