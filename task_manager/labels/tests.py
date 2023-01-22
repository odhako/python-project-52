from django.test import TestCase, Client

# Create your tests here.
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
