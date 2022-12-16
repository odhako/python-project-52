from django.test import TestCase, Client

from task_manager.models import Status, Label


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


class TestDeleting(TestCase):

    def setUp(self):
        self.client.post(
            '/users/create/',
            data={
                'first_name': 'Odhako',
                'last_name': 'Default',
                'username': 'odhako',
                'password1': 'default',
                'password2': 'default',
            }
        )

        self.client.login(username='odhako', password='default')
        self.client.post('/statuses/create/', data={'name': 'Status 001'})
        self.client.post(
            '/tasks/create/',
            data={
                'name': 'task 13',
                'status': 1,
            }
        )

    def test_cant_delete(self):
        status = Status.objects.get(name='Status 001')
        self.client.post(f'/statuses/{status.id}/delete/')
        statuses = Status.objects.all()
        self.assertTrue(statuses)
        print('Status is not deleting when in use: OK')
