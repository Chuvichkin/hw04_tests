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
                text='Тестовый текст0',
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
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': 'test_slug0'}):
            'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': 'Test_User'}):
            'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': 1}):
            'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': 1}):
            'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        # Проверяем, что при обращении к name вызывается HTML-шаблон
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # Проверка словаря контекста страниц
    def test_index_page_show_correct_context(self):
        """index,group_list,profile с правильным контекстом."""
        pages_names = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'test_slug0'}),
            reverse('posts:profile', kwargs={'username': 'Test_User'}),
        ]
        for template in pages_names:
            with self.subTest(template=template):
                response = self.guest_client.get(template)
                first_object = response.context['page_obj'][0]
                task_author_0 = first_object.author.username
                task_text_0 = first_object.text
                task_group_0 = first_object.group.title
                self.assertEqual(task_author_0, 'Test_User')
                self.assertEqual(task_text_0, 'Тестовый текст0')
                self.assertEqual(task_group_0, 'группа0')

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        post_id = 1
        response = self.authorized_client.get(reverse('posts:post_detail',
                                                      args=[post_id]))
        post = response.context['post']
        self.assertEqual(post.pk, post_id)

    def test_create_post_edit_show_correct_context(self):
        """Шаблон create_post(edit) сформирован с правильным контекстом."""
        post_id = 1
        response = self.authorized_client.get(reverse('posts:post_edit',
                                                      args=[post_id]))
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

    def test_urls_first_page_contains_10_records(self):
        """10 постов на страницу у index, group_page and profile"""
        pages_names = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'test_slug0'}),
            reverse('posts:profile', kwargs={'username': 'Test_User'}),
        ]
        for template in pages_names:
            with self.subTest(template=template):
                response = self.guest_client.get(template)
                self.assertEqual(len(response.context['page_obj']), 10)

    def test_urls_second_page_contains_3_records(self):
        """3 поста на второй странице index, group_page and profile"""
        pages_names = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'test_slug0'}),
            reverse('posts:profile', kwargs={'username': 'Test_User'}),
        ]
        for template in pages_names:
            with self.subTest(template=template):
                response = self.guest_client.get(template + '?page=2')
                self.assertEqual(len(response.context['page_obj']), 3)

    def test_post_in_index_group_profile_after_create(self):
        """созданный пост появился на главной, в группе, в профиле."""
        reverse_page_names_post = {
            reverse('posts:index'): self.group.slug,
            reverse('posts:group_list', kwargs={'slug': self.group.slug}):
            self.group.slug,
            reverse('posts:profile', kwargs={'username': self.user}):
            self.group.slug
        }
        for value, expected in reverse_page_names_post.items():
            response = self.authorized_client.get(value)
            for object in response.context['page_obj']:
                post_group = object.group.slug
                with self.subTest(value=value):
                    self.assertEqual(post_group, expected)

    def test_post_not_in_foreign_group(self):
        """Созданного поста НЕТ в чужой группе"""
        Group.objects.create(
            title='группа777',
            slug='test_slug777',
            description='проверка описания777',
        )
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test_slug777'})
        )
        for object in response.context['page_obj']:
            post_slug = object.group.slug
            self.assertNotEqual(post_slug, self.group.slug)
