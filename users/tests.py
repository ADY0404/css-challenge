from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Profile


class AuthenticationFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            email='student@example.edu',
            password='Password123!',
            first_name='Grace',
            last_name='Hopper',
        )
        self.profile = Profile.objects.create(
            user=self.user,
            year=3,
            department='Computer Science',
            bio='Lover of compilers and systems.',
        )

    def test_signup_creates_user_profile_and_signs_user_in(self):
        response = self.client.post(reverse('signup'), {
            'first_name': 'Ada',
            'last_name': 'Lovelace',
            'email': 'ada@example.com',
            'username': 'ada',
            'year': '2',
            'password1': 'A-secure-password-123',
            'password2': 'A-secure-password-123',
        })

        self.assertRedirects(response, reverse('home'))
        user = User.objects.get(username='ada')
        self.assertTrue(Profile.objects.filter(user=user, year=2).exists())
        self.assertEqual(self.client.session['_auth_user_id'], str(user.pk))

    def test_login_and_logout(self):
        # Successful login
        response = self.client.post(reverse('login'), {
            'username': 'teststudent',
            'password': 'Password123!',
        })
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(self.client.session['_auth_user_id'], str(self.user.pk))

        # Logout
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_profile_requires_authentication(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

    def test_profile_update_authenticated(self):
        self.client.login(username='teststudent', password='Password123!')
        response = self.client.post(reverse('profile'), {
            'first_name': 'Grace',
            'last_name': 'Brewster',
            'year': 4,
            'department': 'Software Engineering',
            'bio': 'Updated bio text',
            'github_url': 'https://github.com/ghopper',
            'linkedin_url': 'https://linkedin.com/in/ghopper',
        })
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.user.last_name, 'Brewster')
        self.assertEqual(self.profile.year, 4)
        self.assertEqual(self.profile.department, 'Software Engineering')
        self.assertEqual(self.profile.bio, 'Updated bio text')
        self.assertEqual(self.profile.github_url, 'https://github.com/ghopper')

    def test_settings_save_notifications_and_privacy(self):
        self.client.login(username='teststudent', password='Password123!')

        # Notification action
        response = self.client.post(reverse('settings'), {
            'action': 'notifications',
            'email_digest': 'on',
            'challenge_notifications': 'on',
            # internship_notifications left out to test unchecking
        })
        self.assertRedirects(response, reverse('settings'))
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.email_digest)
        self.assertTrue(self.profile.challenge_notifications)
        self.assertFalse(self.profile.internship_notifications)

        # Privacy action
        response = self.client.post(reverse('settings'), {
            'action': 'privacy',
            'show_on_leaderboard': 'on',
        })
        self.assertRedirects(response, reverse('settings'))
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.show_on_leaderboard)
        self.assertFalse(self.profile.public_profile)

    def test_member_public_profile_viewable(self):
        resp = self.client.get(reverse('member_profile', kwargs={'username': 'teststudent'}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Grace Hopper')
        self.assertContains(resp, 'Computer Science')
        self.assertContains(resp, 'Lover of compilers and systems.')

    def test_member_private_profile_restricted(self):
        self.profile.public_profile = False
        self.profile.save()

        # Anonymous user sees private profile notice
        resp = self.client.get(reverse('member_profile', kwargs={'username': 'teststudent'}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'This Profile is Private')

        # But the owner themselves can view it
        self.client.login(username='teststudent', password='Password123!')
        resp_owner = self.client.get(reverse('member_profile', kwargs={'username': 'teststudent'}))
        self.assertEqual(resp_owner.status_code, 200)
        self.assertContains(resp_owner, 'Grace Hopper')
        self.assertContains(resp_owner, 'Edit My Profile')

