from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_author_url_exists_at_desired_location(self):
        """Проверка доступности адреса /page/about/."""
        response = self.guest_client.get('/page/about/author/')
        self.assertEqual(response.status_code, 200)

    def test_about_author_url_uses_correct_template(self):
        """Проверка шаблона для адреса /page/about/."""
        response = self.guest_client.get('/page/about/author/')
        self.assertTemplateUsed(response, 'about/author.html')

    def test_about_tech_url_exists_at_desired_location(self):
        """Проверка доступности адреса /page/about/."""
        response = self.guest_client.get('/page/about/')
        self.assertEqual(response.status_code, 200)

    def test_about_tech_url_uses_correct_template(self):
        """Проверка шаблона для адреса /page/about/."""
        response = self.guest_client.get('/page/about/tech/')
        self.assertTemplateUsed(response, 'about/tech.html')
