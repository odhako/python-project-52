from django.test import TestCase, Client

# Create your tests here.
from task_manager.statuses.models import Status


class StatusesTest(TestCase):

    def setUp(self):
        self.client.post(
            '/users/create/',
            data={
                'first_name': 'Batman',
                'last_name': 'Suparman',
                'username': 'user_666',
                'password1': 'password_666',
                'password2': 'password_666',
            }
        )
        self.client.login(username='user_666', password='password_666')

    def test_crud_status(self):
        self.client.post('/statuses/create/', data={'name': 'Burned in hell'})
        status = Status.objects.get(name='Burned in hell')
        self.assertEqual(status.name, 'Burned in hell')
        print('Status create: OK')

        self.client.post(f'/statuses/{status.id}/update/', data={'name': 'Lol'})
        status = Status.objects.get(id=status.id)
        self.assertEqual(status.name, 'Lol')
        print('Status update: OK')

        self.client.post(f'/statuses/{status.id}/delete/')
        self.assertFalse(Status.objects.filter(id=status.id).exists())
        print('Status delete: OK')

    def test_logged_out(self):
        c = Client()
        c.post('/logout/')
        response = c.get('/statuses/', follow=True)
        self.assertRedirects(response, '/login/?next=/statuses/')
        print('Redirect unauthorised from /statuses/: OK')
