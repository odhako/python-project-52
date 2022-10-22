from django.test import TestCase, Client
from django.contrib.auth import get_user_model, get_user, login

# Create your tests here.


class BasicTest(TestCase):

    def test_basic(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)


class RegistrationTest(TestCase):

    def setUp(self):
        self.client.post(
            '/users/create/',
            data={
                'first_name': 'firstname1',
                'last_name': 'lastname1',
                'username': 'username1',
                'password1': 'password1',
                'password2': 'password1',
            }
        )

        self.client.post(
            '/users/create/',
            data={
                'first_name': 'firstname2',
                'last_name': 'lastname2',
                'username': 'username2',
                'password1': 'password2',
                'password2': 'password2',
            }
        )

    def test_sign_up(self):
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 2)
        print('Sign up OK')

    def test_login(self):
        self.client.post(
            '/login/',
            data={'username': 'username1', 'password': 'password1'}
        )
        self.assertEqual(get_user(self.client).username, 'username1')
        print('Login OK')

    def test_update_user(self):
        self.client.login(username='username1', password='password1')
        users = get_user_model().objects.filter(username='username1')
        user_id = users[0].id
        self.client.post(
            f'/users/{user_id}/update/',
            data={
                'first_name': 'John',
                'last_name': 'McClane',
                'username': 'diehard',
                'password1': 'Yippee Ki-Yay',
                'password2': 'Yippee Ki-Yay',
            }
        )

        self.assertEqual(
            get_user_model().objects.filter(id=user_id)[0].username,
            'diehard'
        )

        print('Update user OK')

    def test_delete_user(self):
        self.client.login(username='username1', password='password1')
        users = get_user_model().objects.filter(username='username1')
        user_id = users[0].id
        self.client.post(
            f'/users/{user_id}/delete/'
        )
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)
        print('Delete user OK')
