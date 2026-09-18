from django.test import TestCase
from django.urls import reverse
from .models import Executive


class ExecutivesTests(TestCase):
    def setUp(self):
        self.exec_member = Executive.objects.create(
            name='Olumide Johnson',
            position='President',
            academic_year='2024/25',
        )
        self.past_exec = Executive.objects.create(
            name='Blessing Eze',
            position='Vice President',
            academic_year='2023/24',
        )

    def test_executives_list_default_year(self):
        response = self.client.get(reverse('executives:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Olumide Johnson')
        self.assertContains(response, 'President')

    def test_executives_filter_by_year(self):
        response = self.client.get(reverse('executives:list'), {'year': '2023/24'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Blessing Eze')
        self.assertNotContains(response, 'Olumide Johnson')
