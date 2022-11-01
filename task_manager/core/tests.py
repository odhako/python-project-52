from django.test import TestCase, Client
from .models import Status, Task

# Create your tests here.


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
        self.client.post('/statuses/create/', data={'name': 'Burned in hell',})
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


class TasksTest(TestCase):

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

        self.client.post(
            '/users/create/',
            data={
                'first_name': 'Spider',
                'last_name': 'Man',
                'username': 'spidey',
                'password1': 'responsibility',
                'password2': 'responsibility',
            }
        )

        self.client.login(username='user_666', password='password_666')
        self.client.post('/statuses/create/', data={'name': 'Created'})

    def test_crud_task(self):
        self.client.post(
            '/tasks/create/',
            data={
                'name': 'task 13',
                'status': 1
            }
        )

        task = Task.objects.get(name='task 13')
        self.assertEqual(task.name, 'task 13')
        print('Task create: OK')

        self.client.post(
            f'/tasks/{task.id}/update/',
            data={
                'name': 'task 666',
                'status': 1
            }
        )

        task = Task.objects.get(id=task.id)
        self.assertEqual(task.name, 'task 666')
        print('Task update: OK')

        self.client.post(f'/tasks/{task.id}/delete/')
        self.assertFalse(Task.objects.filter(id=task.id).exists())
        print('Task delete: OK')

    def test_other_user_task(self):
        self.client.post(
            '/tasks/create/',
            data={
                'name': 'task 0001',
                'status': 1
            }
        )
        self.client.logout()

        self.client.login(username='spidey', password='responsibility')
        task = Task.objects.get(name='task 0001')
        self.client.post(
            f'/tasks/{task.id}/update/',
            data={
                'name': 'task 0001',
                'description': 'desc',
                'status': 1
            }
        )

        task = Task.objects.get(name='task 0001')
        self.assertEqual(task.description, 'desc')
        print("User can update other user's task: OK")

        response = self.client.post(f'/tasks/{task.id}/delete/')
        self.assertRedirects(
            response,
            '/tasks/'
        )
        print("User can't delete other user's task: OK")
