from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Post, Group

User = get_user_model()


class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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

    def setUp(self):
        # Создаем неавторизованный+авторизованый клиент
        self.guest_client = Client()
        self.user = User.objects.get(username="Test_User")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse('posts:group_list', kwargs={'slug': 'test_slug0'}),
            'posts/profile.html': reverse('posts:profile', kwargs={'username': 'Test_User'}),
            'posts/post_detail.html': reverse('posts:post_detail', kwargs={'post_id': 1}),
            'posts/create_post.html': reverse('posts:post_edit', kwargs={'post_id': 1}),
            'posts/create_post.html': reverse('posts:create_post'),
        }
        # Проверяем, что при обращении к name вызывается соответствующий HTML-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # Проверка словаря контекста главной страницы    
    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        # Взяли первый элемент из списка и проверили, что его содержание
        # совпадает с ожидаемым
        first_object = response.context['page_obj'][0]
        task_author_0 = first_object.author
        task_text_0 = first_object.text
        task_group_0 = first_object.group
        self.assertEqual(task_author_0, 'Test_User')
        self.assertEqual(task_text_0, 'Тестовый текст1')
        self.assertEqual(task_group_0, 'one_group')

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:group_list', kwargs={'slug': 'one_group'}))
        # Взяли первый элемент из списка и проверили, что его содержание
        # совпадает с ожидаемым
        first_object = response.context['page_obj'][0]
        task_author_0 = first_object.author
        task_text_0 = first_object.text
        task_group_0 = first_object.group
        self.assertEqual(task_author_0, 'Test_User')
        self.assertEqual(task_text_0, 'Тестовый текст1')
        self.assertEqual(task_group_0, 'one_group')

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:profile', kwargs={'username': 'Test_User'}))
        # Взяли первый элемент из списка и проверили, что его содержание
        # совпадает с ожидаемым
        first_object = response.context['page_obj'][0]
        task_author_0 = first_object.author
        task_text_0 = first_object.text
        task_group_0 = first_object.group
        self.assertEqual(task_author_0, 'Test_User')
        self.assertEqual(task_text_0, 'Тестовый текст1')
        self.assertEqual(task_group_0, 'one_group')

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        post_id = 1
        response = self.authorized_client.get(reverse('posts:post_detail', args=[post_id]))
        post = response.context['post']
        self.assertEqual(post.pk, post_id)

    def test_create_post_edit_show_correct_context(self):
        """Шаблон create_post(edit) сформирован с правильным контекстом."""
        post_id = 1
        response = self.authorized_client.get(reverse('posts:post_edit', args=[post_id]))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_create_post_show_correct_context(self):
        """Шаблон create_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_urls_first_page_contains_ten_records(self):
        """10 posts are displayed on the first page of index, group_page and profile."""
        pages_names = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'test_slug0'}),
            reverse('posts:profile', kwargs={'username': 'HasNoName'}),
        ]

        for template in pages_names:
            with self.subTest(template=template):
                response = self.guest_client.get(template)
                self.assertEqual(len(response.context['page_obj']), 10)

    def test_urls_second_page_contains_two_records(self):
        """2 posts are displayed on the second page of index, group_page and profile."""
        pages_names = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'test_slug0'}),
            reverse('posts:profile', kwargs={'username': 'Test_User'}),
        ]

        for template in pages_names:
            with self.subTest(template=template):
                response = self.guest_client.get(template + '?page=2')
                self.assertEqual(len(response.context['page_obj']), 3)
