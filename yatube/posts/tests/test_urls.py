from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Post, Group

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        User.objects.create(username="Test_User",)

        Group.objects.create(
            title="группа",
            slug="one_group",
            description="проверка описания",
        )

        Post.objects.create(
            text='Тестовый текст',
            author=User.objects.get(username="Test_User"),
            group=Group.objects.get(title="группа"),
            # post_id='test-post_id'
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованый клиент
        self.user = User.objects.get(username="Test_User")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем общедоступные страницы
    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_url_exists_at_desired_location(self):
        """Страница /group/one_group/ доступна любому пользователю."""
        response = self.guest_client.get('/group/one_group/')
        self.assertEqual(response.status_code, 200)

    def test_user_profile_url_exists_at_desired_location(self):
        """Страница /profile/Test_User/ доступна любому пользователю."""
        response = self.guest_client.get('/profile/Test_User/')
        self.assertEqual(response.status_code, 200)

    def test_post_url_exists_at_desired_location(self):
        """Страница /posts/1/ доступна любому пользователю."""
        response = self.guest_client.get('/posts/1/')
        self.assertEqual(response.status_code, 200)

    # Проверяем доступность страниц для авторизованного пользователя
    def test_post_create_url_exists_at_desired_location(self):
        """Страница /create/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    # Проверяем доступность страниц для АВТОРА?
    def test_post_edit_url_avaliable_only_author(self):
        """Страница /posts/test-post_id/edit/ доступна АВТОРУ."""
        response = self.authorized_client.get('/posts/1/edit/')
        self.assertEqual(response.status_code, 200)

    # Проверяем статус 404 для авторизованного пользователя
    def test_task_list_url_redirect_anonymous(self):
        """Страница /unexisting_page/ не существует."""
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    # Проверка вызываемых шаблонов для каждого адреса
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/one_group/': 'posts/group_list.html',
            '/profile/Test_User/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/posts/1/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
