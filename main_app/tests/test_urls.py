from django.test import TestCase

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main_app.views import index


class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)
