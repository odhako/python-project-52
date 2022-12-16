from django.test import TestCase, Client

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class LabelsTest(TestCase):

    def setUp(self):
        self.client.post(
            '/users/create/',
            data={
                'first_name': 'Spiderman',
                'last_name': 'Iranman',
                'username': 'user_777',
                'password1': 'password_777',
                'password2': 'password_777',
            }
        )
        self.client.login(username='user_777', password='password_777')

    def test_crud_label(self):
        self.client.post('/labels/create/', data={'name': 'TODO'})
        label = Label.objects.get(name='TODO')
        self.assertEqual(label.name, 'TODO')
        print('Label create: OK')

        self.client.post(f'/labels/{label.id}/update/', data={'name': 'NOT DO'})
        label = Label.objects.get(id=label.id)
        self.assertEqual(label.name, 'NOT DO')
        print('Label update: OK')

        self.client.post(f'/labels/{label.id}/delete/')
        self.assertFalse(Status.objects.filter(id=label.id).exists())
        print('Label delete: OK')

    def test_logged_out(self):
        c = Client()
        c.post('/logout/')
        response = c.get('/labels/', follow=True)
        self.assertRedirects(response, '/login/?next=/labels/')
        print('Redirect unauthorised from /labels/: OK')


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
        self.client.post('/labels/create/', data={'name': 'Label 002'})
        self.client.post(
            '/tasks/create/',
            data={
                'name': 'task 13',
                'status': 1,
                'labels': [1, ]
            }
        )

    def test_cant_delete(self):
        label = Label.objects.get(name='Label 002')
        self.client.post(f'/labels/{label.id}/delete/')
        labels = Label.objects.all()
        self.assertTrue(labels)
        print('Label is not deleting when in use: OK')
