from django.test import TestCase

from task_manager.tasks.models import Task


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
