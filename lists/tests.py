from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve

from .views import home_page

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        # Django Test Client로 불러온 응답일 경우에만 동작하는 것에 주의
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

        #request = HttpRequest()
        #response = home_page(request)
        #html = response.content.decode('utf8')

        #self.assertTrue(html.startswith('<html>'))
        #self.assertIn('<title>일정관리</title>', html)
        #self.assertTrue(html.endswith('</html>'))

        #expected_html = render_to_string('home.html')
        #self.assertEqual(html, expected_html)

