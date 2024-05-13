from django.test import TestCase, Client
from django.urls import reverse

class MyViewTestCase(TestCase):
    def test_my_view(self):
        client = Client()
        response = client.get(reverse('admin'))  # замените my_view_name на имя вашего представления
        self.assertEqual(response.status_code, 200)
