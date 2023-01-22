from django.contrib.auth import get_user_model, get_user
from django.test import TestCase, Client
from .models import Task, Label
from .statuses.models import Status


# Create your tests here.


class BasicTest(TestCase):

    def test_basic(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)


class RegistrationTest(TestCase):

    def test_crud_users(self):
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

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 2)
        print('Sign up OK')

        self.client.post(
            '/login/',
            data={'username': 'username1', 'password': 'password1'}
        )
        self.assertEqual(get_user(self.client).username, 'username1')
        print('Login OK')

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

        self.assertEqual(get_user(self.client).username, '')
        print('Logout after update OK')

        self.client.post(
            '/login/',
            data={'username': 'diehard', 'password': 'Yippee Ki-Yay'}
        )
        self.assertEqual(get_user(self.client).username, 'diehard')
        print('Login after update OK')

        users = get_user_model().objects.filter(username='diehard')
        user_id = users[0].id

        self.client.post(f'/users/{user_id}/delete/')
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)
        print('Delete user OK')


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


class TestFilter(TestCase):

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
        self.client.post('/labels/create/', data={'name': 'Label 003'})
        self.client.post(
            '/tasks/create/',
            data={'name': 'Task with 002', 'status': 1, 'labels': [1, ]}
        )
        self.client.post(
            '/tasks/create/',
            data={'name': 'Task with 003', 'status': 1, 'labels': [2, ]}
        )

    def test_filter(self):
        response = self.client.get('/tasks/?status=&executor=&label=1')
        self.assertEqual(response.context['tasks'][0].name, 'Task with 002')
        print('Filtering with querystring: OK')

        response = self.client.get(
            '/tasks/',
            data={'status': '', 'executor': '', 'label': '1'}
        )
        self.assertEqual(response.context['tasks'][0].name, 'Task with 002')
        print('Filtering with form: OK')
