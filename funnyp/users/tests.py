from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()

class UsersViewsTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('testuser', 'testuser@invalid.com', 'passwordtest')

    def test_register_view(self):
        data = { 'username':'testuser1', 'email':'testuser@somemail.com', 'password1':'passwordtest', 'password2':'passwordtest'}
        response = self.client.post(reverse('register'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.get('PATH_INFO'), reverse('login'))

    def test_profile_view(self):
        self.client.login(username=self.user1.username, password='passwordtest')
        response = self.client.post(reverse('profile'), {'username':'testuser2', 'email':'testuser2@invalid.com'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.get('PATH_INFO'), reverse('profile'))


        
