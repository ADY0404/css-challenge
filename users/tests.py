import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from .models import Profile


class AuthenticationFlowTests(TestCase):
    def setUp(self):
        cache.clear()
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
            email_verified=True,
        )

    def tearDown(self):
        cache.clear()

    def test_signup_creates_user_profile_and_redirects_to_verification_pending(self):
        response = self.client.post(reverse('signup'), {
            'first_name': 'Ada',
            'last_name': 'Lovelace',
            'email': 'ada@example.com',
            'username': 'ada',
            'year': '2',
            'password1': 'A-secure-password-123',
            'password2': 'A-secure-password-123',
        })

        self.assertRedirects(response, reverse('email_verification_pending'))
        user = User.objects.get(username='ada')
        self.assertTrue(Profile.objects.filter(user=user, year=2).exists())
        self.assertFalse(user.profile.email_verified)
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(self.client.session['pending_verification_email'], 'ada@example.com')

    def test_signup_with_postgrad_year(self):
        response = self.client.post(reverse('signup'), {
            'first_name': 'Alan',
            'last_name': 'Turing',
            'email': 'alan@example.com',
            'username': 'alan',
            'year': '5',
            'password1': 'A-secure-password-123',
            'password2': 'A-secure-password-123',
        })
        self.assertRedirects(response, reverse('email_verification_pending'))
        user = User.objects.get(username='alan')
        self.assertEqual(user.profile.year, 5)
        self.assertEqual(user.profile.year_display, 'Postgrad')

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

    def test_profile_password_change_requires_old_password(self):
        self.client.login(username='teststudent', password='Password123!')
        response = self.client.post(reverse('profile'), {
            'first_name': 'Grace',
            'last_name': 'Hopper',
            'password': 'NewPassword123!',
            # old_password omitted
        })
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('Password123!'))
        self.assertFalse(self.user.check_password('NewPassword123!'))

    def test_profile_password_change_wrong_old_password(self):
        self.client.login(username='teststudent', password='Password123!')
        response = self.client.post(reverse('profile'), {
            'first_name': 'Grace',
            'last_name': 'Hopper',
            'old_password': 'WrongPassword999!',
            'password': 'NewPassword123!',
        })
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('Password123!'))
        self.assertFalse(self.user.check_password('NewPassword123!'))

    def test_profile_password_change_success(self):
        self.client.login(username='teststudent', password='Password123!')
        response = self.client.post(reverse('profile'), {
            'first_name': 'Grace',
            'last_name': 'Hopper',
            'old_password': 'Password123!',
            'password': 'NewPassword123!',
        })
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPassword123!'))
        # Ensure session auth hash was updated so user remains logged in
        self.assertEqual(self.client.session['_auth_user_id'], str(self.user.pk))

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

    def test_duplicate_email_signup_rejected(self):
        # Case-insensitive duplicate email
        response = self.client.post(reverse('signup'), {
            'first_name': 'Grace',
            'last_name': 'Hopper',
            'email': 'STUDENT@EXAMPLE.EDU',
            'username': 'grace_dup',
            'year': '1',
            'password1': 'ValidPassword123!',
            'password2': 'ValidPassword123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You already have an account. kindly reset your password")
        self.assertFalse(User.objects.filter(username='grace_dup').exists())

    def test_duplicate_email_orm_rejected(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                username='second_student',
                email='student@example.edu',
                password='AnotherPassword123!',
            )

    def test_signup_sends_verification_email_and_marks_unverified(self):
        mail.outbox.clear()
        response = self.client.post(reverse('signup'), {
            'first_name': 'Katherine',
            'last_name': 'Johnson',
            'email': 'kjohnson@example.edu',
            'username': 'kjohnson',
            'year': '3',
            'password1': 'SafePassword123!',
            'password2': 'SafePassword123!',
        })
        self.assertRedirects(response, reverse('email_verification_pending'))
        user = User.objects.get(username='kjohnson')
        self.assertFalse(user.profile.email_verified)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Confirm Ownership of Your Email Address', mail.outbox[0].subject)
        self.assertIn('/u/a-3e7b/', mail.outbox[0].body)

        # Test the email confirmation pending page renders cleanly
        pending_resp = self.client.get(reverse('email_verification_pending'))
        self.assertEqual(pending_resp.status_code, 200)
        self.assertContains(pending_resp, "Kindly Confirm Your Email")
        self.assertContains(pending_resp, "kjohnson@example.edu")

        # Test resending verification with pending page referer stays on pending page
        resend_resp = self.client.post(
            reverse('resend_verification'),
            {'email': 'kjohnson@example.edu'},
            HTTP_REFERER=reverse('email_verification_pending')
        )
        self.assertRedirects(resend_resp, reverse('email_verification_pending'))
        self.assertEqual(len(mail.outbox), 2)

    def test_activate_account_valid_token(self):
        new_user = User.objects.create_user(
            username='margaret',
            email='mhamilton@example.edu',
            password='Password123!',
        )
        profile = Profile.objects.create(user=new_user, year=4)
        self.assertFalse(profile.email_verified)

        uidb64 = urlsafe_base64_encode(force_bytes(new_user.pk))
        token = default_token_generator.make_token(new_user)
        activate_url = reverse('activate_account', kwargs={'uidb64': uidb64, 'token': token})

        response = self.client.get(activate_url)
        self.assertRedirects(response, reverse('home'))
        profile.refresh_from_db()
        self.assertTrue(profile.email_verified)

    def test_activate_account_after_login_succeeds(self):
        """Verify activation token remains valid even after user logs in and last_login updates."""
        from users.tokens import email_verification_token_generator
        new_user = User.objects.create_user(
            username='adabugfix',
            email='adabugfix@example.edu',
            password='Password123!',
        )
        profile = Profile.objects.create(user=new_user, year=2)
        self.assertFalse(profile.email_verified)

        uidb64 = urlsafe_base64_encode(force_bytes(new_user.pk))
        token = email_verification_token_generator.make_token(new_user)

        # User logs in, updating last_login
        self.client.login(username='adabugfix', password='Password123!')

        activate_url = reverse('activate_account', kwargs={'uidb64': uidb64, 'token': token})
        response = self.client.get(activate_url)
        self.assertRedirects(response, reverse('home'))
        profile.refresh_from_db()
        self.assertTrue(profile.email_verified)

    def test_activate_account_invalid_token(self):
        new_user = User.objects.create_user(
            username='hedy',
            email='hlamarr@example.edu',
            password='Password123!',
        )
        profile = Profile.objects.create(user=new_user, year=1)
        uidb64 = urlsafe_base64_encode(force_bytes(new_user.pk))
        bad_token = 'invalid-token-12345'
        activate_url = reverse('activate_account', kwargs={'uidb64': uidb64, 'token': bad_token})

        response = self.client.get(activate_url)
        self.assertRedirects(response, reverse('login'))
        profile.refresh_from_db()
        self.assertFalse(profile.email_verified)

    def test_resend_verification_email(self):
        mail.outbox.clear()
        self.client.login(username='teststudent', password='Password123!')
        self.profile.email_verified = False
        self.profile.save()

        response = self.client.get(reverse('resend_verification'))
        self.assertRedirects(response, reverse('profile'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.user.email, mail.outbox[0].to)

    def test_account_lockout_after_five_failed_attempts(self):
        login_url = reverse('login')
        # 4 incorrect attempts
        for attempt in range(1, 5):
            resp = self.client.post(login_url, {
                'username': 'teststudent',
                'password': 'WrongPassword!',
            })
            self.assertEqual(resp.status_code, 200)
            self.profile.refresh_from_db()
            self.assertEqual(self.profile.failed_login_attempts, attempt)
            self.assertFalse(self.profile.is_locked)

        # 5th incorrect attempt must lock the account
        resp = self.client.post(login_url, {
            'username': 'teststudent',
            'password': 'WrongPassword!',
        })
        self.assertEqual(resp.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.failed_login_attempts, 5)
        self.assertTrue(self.profile.is_locked)
        self.assertContains(resp, "Your account is locked due to 5 incorrect login attempts")

        # Clear IP rate limit before the 6th attempt so we specifically test account lockout
        cache.clear()
        # 6th attempt (even with valid password) is blocked due to active lock
        resp_blocked = self.client.post(login_url, {
            'username': 'teststudent',
            'password': 'Password123!',
        })
        self.assertEqual(resp_blocked.status_code, 200)
        self.assertContains(resp_blocked, "Kindly reset your password to regain access")
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_post_reset_ten_minute_cooldown(self):
        login_url = reverse('login')
        # Simulate completed password reset
        self.profile.schedule_post_reset_cooldown(minutes=10)
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.is_locked)

        cache.clear()
        # Immediate login attempt is rejected with cooldown remaining time
        resp = self.client.post(login_url, {
            'username': 'teststudent',
            'password': 'Password123!',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "will open in")
        self.assertNotIn('_auth_user_id', self.client.session)

        # Fast forward time beyond the 10-minute cooldown
        self.profile.unlock_at = timezone.now() - datetime.timedelta(seconds=5)
        self.profile.save()

        cache.clear()
        # Login now succeeds automatically
        resp_success = self.client.post(login_url, {
            'username': 'teststudent',
            'password': 'Password123!',
        })
        self.assertRedirects(resp_success, reverse('home'))
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.is_locked)
        self.assertEqual(self.profile.failed_login_attempts, 0)
        self.assertEqual(self.client.session['_auth_user_id'], str(self.user.pk))

    def test_admin_unlock_and_verify_actions(self):
        from users.admin import ProfileAdmin
        from django.contrib.admin.sites import AdminSite

        self.profile.is_locked = True
        self.profile.failed_login_attempts = 5
        self.profile.email_verified = False
        self.profile.save()

        admin_instance = ProfileAdmin(Profile, AdminSite())
        qs = Profile.objects.filter(pk=self.profile.pk)

        # Unlock action
        admin_instance.unlock_accounts(None, qs)
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.is_locked)
        self.assertEqual(self.profile.failed_login_attempts, 0)

        # Verify email action
        admin_instance.verify_emails(None, qs)
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.email_verified)

    def test_unverified_user_cannot_login(self):
        unverified_user = User.objects.create_user(
            username='unverified_student',
            email='unverified@example.edu',
            password='Password123!',
        )
        Profile.objects.create(
            user=unverified_user,
            year=1,
            email_verified=False,
        )

        cache.clear()
        response = self.client.post(reverse('login'), {
            'username': 'unverified_student',
            'password': 'Password123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your email address is not verified")
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_admin_can_login_even_if_unverified(self):
        admin_user = User.objects.create_user(
            username='admin_boss',
            email='admin@example.edu',
            password='AdminPassword123!',
            is_staff=True,
        )
        Profile.objects.create(
            user=admin_user,
            year=4,
            email_verified=False,
        )

        cache.clear()
        response = self.client.post(reverse('login'), {
            'username': 'admin_boss',
            'password': 'AdminPassword123!',
        })
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(self.client.session['_auth_user_id'], str(admin_user.pk))

    def test_unauthenticated_resend_verification_email(self):
        mail.outbox.clear()
        unverified_user = User.objects.create_user(
            username='need_resend',
            email='resend@example.edu',
            password='Password123!',
        )
        Profile.objects.create(user=unverified_user, year=2, email_verified=False)

        cache.clear()
        response = self.client.post(reverse('resend_verification'), {
            'email': 'resend@example.edu'
        })
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('resend@example.edu', mail.outbox[0].to)

    def test_password_reset_page_renders_username_or_email_options(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'opt_email')
        self.assertContains(response, 'opt_username')
        self.assertContains(response, 'username_or_email')

    def test_password_reset_by_email_dispatches_email(self):
        mail.outbox.clear()
        response = self.client.post(reverse('password_reset'), {
            'username_or_email': 'student@example.edu',
        })
        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('student@example.edu', mail.outbox[0].to)
        self.assertIn('password', mail.outbox[0].body.lower())
        self.assertTrue(any('Reset Password' in alt[0] for alt in getattr(mail.outbox[0], 'alternatives', [])))

    def test_password_reset_by_username_dispatches_to_associated_email(self):
        mail.outbox.clear()
        response = self.client.post(reverse('password_reset'), {
            'username_or_email': 'teststudent',
        })
        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('student@example.edu', mail.outbox[0].to)

    def test_admin_route_is_adcs_and_old_admin_is_404(self):
        # /adcs/ should render the admin login page
        resp_adcs = self.client.get('/adcs/')
        self.assertIn(resp_adcs.status_code, [200, 302])
        # /admin/ should now return 404
        resp_old = self.client.get('/admin/')
        self.assertEqual(resp_old.status_code, 404)

    def test_account_deactivation_with_valid_password(self):
        self.client.login(username='teststudent', password='Password123!')
        response = self.client.post(reverse('settings'), {
            'action': 'deactivate',
            'confirm_password': 'Password123!',
        })
        self.assertRedirects(response, reverse('home'))
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        # Session is logged out
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_account_deactivation_fails_with_invalid_password(self):
        self.client.login(username='teststudent', password='Password123!')
        response = self.client.post(reverse('settings'), {
            'action': 'deactivate',
            'confirm_password': 'WrongPassword!',
        })
        self.assertRedirects(response, reverse('settings'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_deactivated_account_login_is_blocked_with_message(self):
        self.user.is_active = False
        self.user.save()
        cache.clear()
        response = self.client.post(reverse('login'), {
            'username': 'teststudent',
            'password': 'Password123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This account has been deactivated')

    def test_obfuscated_urls_resolve_properly(self):
        self.assertEqual(reverse('profile'), '/u/p-8f2a7b/')
        self.assertEqual(reverse('settings'), '/u/s-4d91ae/')
        self.assertEqual(reverse('password_reset'), '/u/r-5b2f9a/')
        self.assertEqual(reverse('member_profile', kwargs={'username': 'teststudent'}), '/u/m-6c3e81/teststudent/')

    def test_legacy_and_home_users_redirect_to_obfuscated_routes(self):
        resp_home_users = self.client.get('/home/users/')
        self.assertRedirects(resp_home_users, '/u/p-8f2a7b/', fetch_redirect_response=False)

        resp_old_profile = self.client.get('/users/profile/')
        self.assertRedirects(resp_old_profile, '/u/p-8f2a7b/', fetch_redirect_response=False)

        resp_old_settings = self.client.get('/users/settings/')
        self.assertRedirects(resp_old_settings, '/u/s-4d91ae/', fetch_redirect_response=False)

    def test_admin_can_reactivate_deactivated_account(self):
        admin_user = User.objects.create_superuser('admin_tester', 'admin@example.edu', 'AdminPass123!')
        self.user.is_active = False
        self.user.save()
        self.profile.is_locked = True
        self.profile.failed_login_attempts = 5
        self.profile.save()

        self.client.login(username='admin_tester', password='AdminPass123!')
        reactivate_url = reverse('admin:user_reactivate', args=[self.user.pk])
        response = self.client.get(reactivate_url)
        self.assertIn(response.status_code, [200, 302])

        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.profile.is_locked)
        self.assertEqual(self.profile.failed_login_attempts, 0)

    def test_admin_can_deactivate_and_unlock_via_views(self):
        admin_user = User.objects.create_superuser('admin_tester2', 'admin2@example.edu', 'AdminPass123!')
        self.client.login(username='admin_tester2', password='AdminPass123!')

        deactivate_url = reverse('admin:user_deactivate', args=[self.user.pk])
        self.client.get(deactivate_url)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

        unlock_url = reverse('admin:user_unlock', args=[self.user.pk])
        self.client.get(unlock_url)
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.profile.is_locked)



