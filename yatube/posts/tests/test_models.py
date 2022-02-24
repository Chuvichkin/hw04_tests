from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )


    def test_models_have_correct_object_names(self):
        """__str__  task - это строчка с содержимым task.title."""
        group = PostModelTest.group  # Обратите внимание на синтаксис
        expected_object_name_group = group.title
        self.assertEqual(expected_object_name_group, str(group))
        
        post = PostModelTest.post  # Обратите внимание на синтаксис
        expected_object_name_post = post.text[:15]
        self.assertEqual(expected_object_name_post, str(post))
        """Проверяем, что у моделей корректно работает __str__."""
