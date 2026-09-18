from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Event, GuestSpeaker, EventRegistration


class ActivitiesTests(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            title='Web Development Workshop',
            time='10:00:00',
            description='Build a modern responsive portfolio.',
            activity='Hands-on coding workshop with CSS mentors.',
            date=timezone.now().date() + timezone.timedelta(days=7),
            button_text='View Workshop',
        )
        self.speaker = GuestSpeaker.objects.create(
            name='Tunde Balogun',
            title='Staff Engineer @ TechCorp',
            event=self.event,
        )

    def test_activities_list(self):
        response = self.client.get(reverse('act:activities_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Web Development Workshop')

    def test_event_detail(self):
        response = self.client.get(reverse('act:event', kwargs={'id': self.event.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Web Development Workshop')
        self.assertContains(response, 'Tunde Balogun')

    def test_event_registration_post(self):
        response = self.client.post(reverse('act:event_register', kwargs={'id': self.event.id}), {
            'full_name': 'Kemi Adeleke',
            'email': 'kemi@university.edu',
            'year': 2,
        })
        self.assertRedirects(response, reverse('act:event', kwargs={'id': self.event.id}))
        reg = EventRegistration.objects.get(event=self.event, email='kemi@university.edu')
        self.assertEqual(reg.full_name, 'Kemi Adeleke')
        self.assertEqual(reg.year, 2)
