import shutil
import tempfile

from posts.forms import PostForm
from posts.models import Post
from django.test import Client, TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model
from posts.models import Post, Group
User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # Создадим запись в БД
        cls.user = User.objects.create(username="Test_User",)

        cls.group = Group.objects.create(
            title="группа0",
            slug="test_slug0",
            description="проверка описания0",
        )

        for i in range(13):
            cls.post = Post.objects.create(
                text='Тестовый текст' + str(i),
                author=cls.user,
                group=Group.objects.get(slug='test_slug0'),
                # post_id='test-post_id'
            )
        # Создаем форму, если нужна проверка атрибутов
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Модуль shutil - библиотека Python с удобными инструментами 
        # для управления файлами и директориями: 
        # создание, удаление, копирование, перемещение, изменение папок и файлов
        # Метод shutil.rmtree удаляет директорию и всё её содержимое
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()

    def test_create_post(self):
        """Валидная форма создает запись в Posts."""
        # Подсчитаем количество записей в Posts
        posts_count = Post.objects.count()

        form_data = {
            'text': 'Тестовый текст0',
            'group': 'test_slug0',
        }
        # Отправляем POST-запрос
        response = self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        #self.assertRedirects(response, reverse('posts:profile'))
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count + 1)
        # Проверяем, что создалась запись с заданным слагом
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст0',
                group='test_slug0'
            ).exists()
        )

    def test_edit_post(self):
        """Валидная форма создает запись в Task."""
        # Подсчитаем количество записей в Task
        posts_count = Post.objects.count()
        post_id = 1,
        post_old = Post.objects.get(pk='1')

        form_data = {
            'text': 'Тестовый текст2',
            'group': 'test_slug2',
        }
        # Отправляем POST-запрос
        response = self.guest_client.post(
            reverse('posts:post_edit', args=(post_id)),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('posts:post_detail',args=(post_id)))
        # Проверяем, не увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count)
        # Проверяем, что пост изменился
        self.assertNotEqual(Post.objects.get(pk=post_id), post_old)
