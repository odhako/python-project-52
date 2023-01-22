from django.test import TestCase, Client
from .labels.models import Label
from .statuses.models import Status


# Create your tests here.


class BasicTest(TestCase):

    def test_basic(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)


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
        status = Status.objects.get(name='Status 001')
        self.client.post(f'/statuses/{status.id}/delete/')
        statuses = Status.objects.all()
        self.assertTrue(statuses)
        print('Status is not deleting when in use: OK')

        label = Label.objects.get(name='Label 002')
        self.client.post(f'/labels/{label.id}/delete/')
        labels = Label.objects.all()
        self.assertTrue(labels)
        print('Label is not deleting when in use: OK')


