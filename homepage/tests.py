from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import (
    Challenge,
    ChallengeSubmission,
    SubmissionUpvote,
    Article,
    Internship,
    NewsletterSubscriber,
    CommunityMessage,
    CommunityChannel,
    ClinicAppointment,
)


class HomepageViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='codewiz',
            email='codewiz@example.edu',
            password='TestPassword123!',
            first_name='Alan',
            last_name='Turing',
        )

        self.featured_challenge = Challenge.objects.create(
            title='Campus Resource Scheduler',
            slug='campus-resource-scheduler',
            summary='Build a meeting and lab reservation backend.',
            description='Detailed requirements for reservation algorithms.',
            requirements='Write clean code with unit test coverage.',
            category='Design & Dev',
            difficulty='Intermediate',
            is_active=True,
            is_featured=True,
            week_label='Week 04',
            deadline_text='Closes Sunday at 11:59 PM',
        )

        self.article = Article.objects.create(
            title='Getting Started with Django REST',
            slug='getting-started-with-django-rest',
            category='learning',
            author_name='Alan Turing',
            author_role='VP of Education',
            summary='A guide to designing RESTful endpoints.',
            content='Full guide body content with explanations.',
            read_time='6 min read',
            is_featured=True,
        )

        self.internship = Internship.objects.create(
            title='Software Engineer Intern',
            company='Atlas Systems',
            location='Lagos (Hybrid)',
            role_type='Internship',
            description='Work on backend distributed storage.',
            apply_url='https://atlas.example.com/careers',
            tags='Python, Django, PostgreSQL',
            is_featured=True,
        )

    def test_home_page_renders_status_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Campus Resource Scheduler')
        self.assertContains(response, 'Getting Started with Django REST')

    def test_challenges_list_and_detail(self):
        list_resp = self.client.get(reverse('challenge'))
        self.assertEqual(list_resp.status_code, 200)
        self.assertContains(list_resp, 'Campus Resource Scheduler')

        detail_resp = self.client.get(reverse('challenge_detail', kwargs={'slug': 'campus-resource-scheduler'}))
        self.assertEqual(detail_resp.status_code, 200)
        self.assertContains(detail_resp, 'Campus Resource Scheduler')

    def test_challenge_submission_flow(self):
        # Anonymous user redirected to login
        response = self.client.post(reverse('challenge_detail', kwargs={'slug': 'campus-resource-scheduler'}), {
            'project_title': 'My Scheduler App',
            'repo_url': 'https://github.com/codewiz/scheduler',
            'description': 'Implemented with Django ORM',
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

        # Authenticated submission succeeds and persists
        self.client.login(username='codewiz', password='TestPassword123!')
        response = self.client.post(reverse('challenge_detail', kwargs={'slug': 'campus-resource-scheduler'}), {
            'project_title': 'My Scheduler App',
            'repo_url': 'https://github.com/codewiz/scheduler',
            'demo_url': 'https://scheduler.example.com',
            'description': 'Implemented with Django ORM and background workers',
        })
        self.assertRedirects(response, reverse('challenge_detail', kwargs={'slug': 'campus-resource-scheduler'}))
        submission = ChallengeSubmission.objects.get(challenge=self.featured_challenge, user=self.user)
        self.assertEqual(submission.repo_url, 'https://github.com/codewiz/scheduler')
        self.assertEqual(submission.demo_url, 'https://scheduler.example.com')

    def test_blog_list_and_category_filter(self):
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Getting Started with Django REST')

        # Filter by valid category
        filter_resp = self.client.get(reverse('blog'), {'category': 'learning'})
        self.assertEqual(filter_resp.status_code, 200)
        self.assertContains(filter_resp, 'Getting Started with Django REST')

        # Filter by category with no matches
        empty_resp = self.client.get(reverse('blog'), {'category': 'build'})
        self.assertEqual(empty_resp.status_code, 200)
        self.assertNotContains(empty_resp, 'Getting Started with Django REST')

    def test_article_detail(self):
        response = self.client.get(reverse('article_detail', kwargs={'slug': 'getting-started-with-django-rest'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Getting Started with Django REST')
        self.assertContains(response, 'Alan Turing')

    def test_internships_list_and_share_opportunity(self):
        response = self.client.get(reverse('internships'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Atlas Systems')

        # Share new opportunity
        post_resp = self.client.post(reverse('share_opportunity'), {
            'title': 'Frontend Developer Trainee',
            'company': 'Kora Studio',
            'location': 'Remote',
            'role_type': 'Full-time',
            'description': 'React and TypeScript engineering.',
            'apply_url': 'https://kora.example.com/apply',
            'tags': 'React, TypeScript',
        })
        self.assertRedirects(post_resp, reverse('internships'))
        self.assertTrue(Internship.objects.filter(company='Kora Studio').exists())

    def test_newsletter_subscription(self):
        response = self.client.post(reverse('newsletter_subscribe'), {
            'email': 'student@university.edu',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(NewsletterSubscriber.objects.filter(email='student@university.edu').exists())

    def test_community_and_channel_chat(self):
        # Community overview
        resp = self.client.get(reverse('community'))
        self.assertEqual(resp.status_code, 200)

        # Community channel chat
        chat_resp = self.client.get(reverse('community_channel', kwargs={'channel': 'ai-ml'}))
        self.assertEqual(chat_resp.status_code, 200)
        self.assertContains(chat_resp, 'Future of AI &amp; Machine Learning')

        # Post message authenticated
        self.client.login(username='codewiz', password='TestPassword123!')
        msg_resp = self.client.post(reverse('community_channel', kwargs={'channel': 'ai-ml'}), {
            'text': 'Has anyone started on the transformer paper implementation?',
        })
        self.assertRedirects(msg_resp, reverse('community_channel', kwargs={'channel': 'ai-ml'}))
        self.assertTrue(CommunityMessage.objects.filter(
            channel='ai-ml',
            user=self.user,
            text='Has anyone started on the transformer paper implementation?'
        ).exists())

        # Reply to the first message
        first_msg = CommunityMessage.objects.filter(channel='ai-ml').first()
        reply_resp = self.client.post(reverse('community_channel', kwargs={'channel': 'ai-ml'}), {
            'text': 'Yes, I started yesterday using PyTorch.',
            'parent_id': str(first_msg.id),
        })
        self.assertRedirects(reply_resp, reverse('community_channel', kwargs={'channel': 'ai-ml'}))
        reply_msg = CommunityMessage.objects.filter(text='Yes, I started yesterday using PyTorch.').first()
        self.assertIsNotNone(reply_msg)
        self.assertEqual(reply_msg.parent, first_msg)

        # Verify chat view displays reply quote and member profile link
        chat_page = self.client.get(reverse('community_channel', kwargs={'channel': 'ai-ml'}))
        self.assertEqual(chat_page.status_code, 200)
        self.assertContains(chat_page, 'Replying to')
        self.assertContains(chat_page, reverse('member_profile', kwargs={'username': self.user.username}))

    def test_informational_pages(self):
        for page_name in ['guidelines', 'programs', 'terms', 'privacy']:
            resp = self.client.get(reverse(page_name))
            self.assertEqual(resp.status_code, 200)

    def test_programs_page_links_to_clinic_dates(self):
        resp = self.client.get(reverse('programs'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, reverse('clinic_dates'))
        self.assertNotContains(resp, 'href="/activities/" class="btn btn-sm btn-outline-success">View Clinic Dates')

    def test_clinic_dates_renders_successfully(self):
        resp = self.client.get(reverse('clinic_dates'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'PC Clinic &amp; Diagnostic Sessions')
        self.assertContains(resp, 'Software Lab 204')
        self.assertContains(resp, 'Linux Dual-Boot')

    def test_clinic_appointment_booking(self):
        resp = self.client.post(reverse('clinic_dates'), {
            'full_name': 'Grace Hopper',
            'student_email': 'ghopper@university.edu',
            'student_id': '2081920',
            'department': 'Computer Science',
            'academic_year': 'Year 2',
            'device_brand': 'Lenovo',
            'device_model': 'ThinkPad T480',
            'service_type': 'linux',
            'preferred_session': '2024-10-04',
            'issue_description': 'Dual-boot Ubuntu 24.04 alongside Windows 11 with 100GB root partition.',
            'backup_acknowledged': 'on',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('clinic_dates'))

        appointment = ClinicAppointment.objects.filter(student_email='ghopper@university.edu').first()
        self.assertIsNotNone(appointment)
        self.assertEqual(appointment.full_name, 'Grace Hopper')
        self.assertEqual(appointment.device_brand, 'Lenovo')
        self.assertEqual(appointment.device_model, 'ThinkPad T480')
        self.assertTrue(appointment.ticket_id.startswith('CLN-'))

    def test_leaderboard_view_and_rankings(self):
        second_user = User.objects.create_user(
            username='ada_lovelace',
            email='ada@example.edu',
            password='TestPassword123!',
            first_name='Ada',
            last_name='Lovelace',
        )
        second_challenge = Challenge.objects.create(
            title='Recursive Tree Parser',
            slug='recursive-tree-parser',
            summary='Parse nested AST trees.',
            description='Detailed AST specifications.',
            requirements='Clean Python code.',
            category='Algorithms',
            difficulty='Hard',
            is_active=True,
        )

        ChallengeSubmission.objects.create(
            challenge=self.featured_challenge,
            user=self.user,
            project_title='Campus Scheduler Solution',
            repo_url='https://github.com/codewiz/scheduler',
            description='Built with Django.',
        )

        ChallengeSubmission.objects.create(
            challenge=self.featured_challenge,
            user=second_user,
            project_title='Ada Campus Scheduler',
            repo_url='https://github.com/ada/scheduler',
            description='Optimized solver.',
        )
        ChallengeSubmission.objects.create(
            challenge=second_challenge,
            user=second_user,
            project_title='Ada Tree Parser',
            repo_url='https://github.com/ada/tree',
            description='Recursive descent parser.',
        )

        resp = self.client.get(reverse('leaderboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Ada Lovelace')
        self.assertContains(resp, 'Alan Turing')
        self.assertEqual(resp.context['top_three'][0]['user'], second_user)
        self.assertEqual(resp.context['top_three'][0]['submission_count'], 2)

        from users.models import Profile
        ada_profile, _ = Profile.objects.get_or_create(user=second_user)
        ada_profile.show_on_leaderboard = False
        ada_profile.save()

        resp2 = self.client.get(reverse('leaderboard'))
        self.assertEqual(resp2.status_code, 200)
        solver_users = [item['user'] for item in resp2.context['ranked_members']]
        self.assertNotIn(second_user, solver_users)
        self.assertIn(self.user, solver_users)

    def test_upvote_submission_toggle(self):
        sub = ChallengeSubmission.objects.create(
            challenge=self.featured_challenge,
            user=self.user,
            project_title='Scheduler Alpha',
            repo_url='https://github.com/codewiz/alpha',
            description='Initial prototype.',
        )
        upvote_url = reverse('upvote_submission', kwargs={'sub_id': sub.id})

        anon_resp = self.client.post(upvote_url)
        self.assertEqual(anon_resp.status_code, 401)
        self.assertFalse(anon_resp.json()['authenticated'])

        self.client.login(username='codewiz', password='TestPassword123!')
        vote_resp = self.client.post(upvote_url)
        self.assertEqual(vote_resp.status_code, 200)
        data = vote_resp.json()
        self.assertTrue(data['authenticated'])
        self.assertTrue(data['upvoted'])
        self.assertEqual(data['count'], 1)
        self.assertEqual(sub.upvotes.count(), 1)

        unvote_resp = self.client.post(upvote_url)
        self.assertEqual(unvote_resp.status_code, 200)
        data2 = unvote_resp.json()
        self.assertFalse(data2['upvoted'])
        self.assertEqual(data2['count'], 0)
        self.assertEqual(sub.upvotes.count(), 0)

    def test_community_messages_api(self):
        msg1 = CommunityMessage.objects.create(
            channel='ai-ml',
            user=self.user,
            text='Hello world from automated test!',
        )
        api_url = reverse('community_messages_api')

        resp = self.client.get(f"{api_url}?channel=ai-ml&after_id=0")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('messages', data)
        self.assertTrue(any(m['id'] == msg1.id for m in data['messages']))

        resp2 = self.client.get(f"{api_url}?channel=ai-ml&after_id={msg1.id}")
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(len(resp2.json()['messages']), 0)

    def test_global_search_view(self):
        search_url = reverse('search')

        empty_resp = self.client.get(search_url)
        self.assertEqual(empty_resp.status_code, 200)
        self.assertEqual(empty_resp.context['total_results'], 0)

        c_resp = self.client.get(f"{search_url}?q=Scheduler")
        self.assertEqual(c_resp.status_code, 200)
        self.assertGreaterEqual(c_resp.context['challenges_count'], 1)
        self.assertContains(c_resp, 'Campus Resource Scheduler')

        a_resp = self.client.get(f"{search_url}?q=Django")
        self.assertEqual(a_resp.status_code, 200)
        self.assertGreaterEqual(a_resp.context['articles_count'], 1)
        self.assertContains(a_resp, 'Getting Started with Django REST')

        i_resp = self.client.get(f"{search_url}?q=Atlas")
        self.assertEqual(i_resp.status_code, 200)
        self.assertGreaterEqual(i_resp.context['internships_count'], 1)
        self.assertContains(i_resp, 'Atlas Systems')


class AdminPortalTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin_lead',
            email='admin@css.knust.edu',
            password='AdminPassword123!',
        )
        self.client.login(username='admin_lead', password='AdminPassword123!')

    def test_admin_index_renders_custom_branding(self):
        resp = self.client.get('/admin/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Computer Science Society Administration')

    def test_all_models_registered_and_accessible(self):
        from django.contrib import admin
        registered_models = [
            'challenge',
            'challengesubmission',
            'submissionupvote',
            'article',
            'internship',
            'newslettersubscriber',
            'communitymessage',
            'clinicappointment',
            'clinicsession',
            'infopage',
            'communitychannel',
            'siteconfiguration',
        ]
        for model_name in registered_models:
            url = f'/admin/homepage/{model_name}/'
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200, f"Failed to access admin changelist for {model_name}")

    def test_activities_and_executives_accessible_in_admin(self):
        for app, model in [
            ('activities', 'event'),
            ('activities', 'eventregistration'),
            ('activities', 'guestspeaker'),
            ('activities', 'socialmedia'),
            ('activities', 'program'),
            ('executives', 'executive'),
        ]:
            url = f'/admin/{app}/{model}/'
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200, f"Failed to access admin for {app}.{model}")

    def test_user_and_profile_accessible_in_admin(self):
        resp_user = self.client.get('/admin/auth/user/')
        self.assertEqual(resp_user.status_code, 200)
        resp_profile = self.client.get('/admin/users/profile/')
        self.assertEqual(resp_profile.status_code, 200)

    def test_site_configuration_singleton_and_channel_creation(self):
        from homepage.models import SiteConfiguration, CommunityChannel
        config = SiteConfiguration.get_solo()
        config.announcement_text = 'Midsemester Hackathon Registrations Open!'
        config.announcement_active = True
        config.save()

        home_resp = self.client.get(reverse('home'))
        self.assertEqual(home_resp.status_code, 200)
        self.assertContains(home_resp, 'Midsemester Hackathon Registrations Open!')

        # Test creating a new community channel via admin/ORM
        new_channel = CommunityChannel.objects.create(
            name='Quantum Computing Guild',
            slug='quantum-computing',
            category='systems',
            description='Exploring Qiskit, quantum circuits, and quantum algorithms.',
            icon_class='bi-cpu',
            order=10,
            is_active=True,
        )
        comm_resp = self.client.get(reverse('community'))
        self.assertEqual(comm_resp.status_code, 200)
        self.assertContains(comm_resp, 'Quantum Computing Guild')


class CommunityPageAndImageUploadTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='cadet_coder',
            email='cadet@css.edu',
            password='Password123!',
            first_name='Grace',
            last_name='Hopper',
        )

    def _create_image_file(self, size=(200, 200), format='PNG', color='blue'):
        import io
        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile
        buffer = io.BytesIO()
        img = Image.new('RGB', size, color=color)
        img.save(buffer, format=format)
        buffer.seek(0)
        ext = format.lower()
        return SimpleUploadedFile(f"test_hub_icon.{ext}", buffer.read(), content_type=f"image/{ext}")

    def test_community_page_elements_and_modal_present(self):
        self.client.login(username='cadet_coder', password='Password123!')
        resp = self.client.get(reverse('community'))
        self.assertEqual(resp.status_code, 200)
        # Check hero, buttons, and interactive modal presence
        self.assertContains(resp, 'Join a Technical Community')
        self.assertContains(resp, 'data-category="ai"')
        self.assertContains(resp, 'id="proposeHubModal"')
        self.assertContains(resp, 'Propose a Hub')
        self.assertContains(resp, 'id="communitySearchInput"')
        self.assertContains(resp, 'id="clearSearchBtn"')
        self.assertContains(resp, 'Aspect Ratio: <strong>1:1 Square</strong>')

    def test_propose_channel_requires_authentication(self):
        url = reverse('propose_community_channel')
        resp = self.client.post(url, {
            'name': 'Embedded Robotics Hub',
            'category': 'Open Source & Systems',
            'description': 'Building microcontrollers and firmware for automated robots.',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/login/', resp.url)

    def test_propose_channel_rejects_missing_image(self):
        self.client.login(username='cadet_coder', password='Password123!')
        url = reverse('propose_community_channel')
        resp = self.client.post(url, {
            'name': 'Embedded Robotics Hub',
            'category': 'Open Source & Systems',
            'description': 'Building microcontrollers and firmware for automated robots.',
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'A square hub icon or cover image is required')
        self.assertFalse(CommunityChannel.objects.filter(slug='embedded-robotics-hub').exists())

    def test_propose_channel_rejects_non_square_aspect_ratio(self):
        self.client.login(username='cadet_coder', password='Password123!')
        url = reverse('propose_community_channel')
        # 400 x 100 is 4:1 ratio (not square)
        wide_image = self._create_image_file(size=(400, 100), format='PNG')
        resp = self.client.post(url, {
            'name': 'Game Dev Society',
            'category': 'Open Source & Systems',
            'description': 'Creating indie 2D and 3D games with Godot and Unreal Engine.',
            'hub_image': wide_image,
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Image must have an approximate 1:1 square aspect ratio')
        self.assertFalse(CommunityChannel.objects.filter(slug='game-dev-society').exists())

    def test_propose_channel_rejects_unsupported_format(self):
        self.client.login(username='cadet_coder', password='Password123!')
        url = reverse('propose_community_channel')
        from django.core.files.uploadedfile import SimpleUploadedFile
        fake_file = SimpleUploadedFile("malicious.txt", b"not an image", content_type="text/plain")
        resp = self.client.post(url, {
            'name': 'Malware Analysis Hub',
            'category': 'Cybersecurity',
            'description': 'Exploring reverse engineering techniques and malware sandboxing.',
            'hub_image': fake_file,
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'not a valid or readable image')

    def test_propose_channel_success_with_valid_square_image(self):
        self.client.login(username='cadet_coder', password='Password123!')
        url = reverse('propose_community_channel')
        valid_image = self._create_image_file(size=(250, 250), format='PNG')
        resp = self.client.post(url, {
            'name': 'Game Development Collective',
            'category': 'Open Source & Systems',
            'description': 'Creating indie 2D and 3D games with Godot, Unity, and shaders.',
            'hub_image': valid_image,
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'has been successfully created')
        
        created = CommunityChannel.objects.filter(slug='game-development-collective').first()
        self.assertIsNotNone(created)
        self.assertEqual(created.name, 'Game Development Collective')
        self.assertTrue(bool(created.image))

        # Verify it shows up on community page
        comm_resp = self.client.get(reverse('community'))
        self.assertContains(comm_resp, 'Game Development Collective')
        self.assertContains(comm_resp, created.image.url)

    def test_profile_picture_validation_in_users_view(self):
        self.client.login(username='cadet_coder', password='Password123!')
        profile_url = reverse('profile')
        
        # Test non-square image rejection
        wide_image = self._create_image_file(size=(500, 150), format='JPEG')
        resp = self.client.post(profile_url, {
            'profile_picture': wide_image,
            'first_name': 'Grace',
            'last_name': 'Hopper',
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Image must have an approximate 1:1 square aspect ratio')

        # Test valid square profile photo upload
        valid_photo = self._create_image_file(size=(200, 200), format='JPEG')
        resp2 = self.client.post(profile_url, {
            'profile_picture': valid_photo,
            'first_name': 'Grace',
            'last_name': 'Hopper',
        }, follow=True)
        self.assertEqual(resp2.status_code, 200)
        self.assertContains(resp2, 'Your profile has been updated successfully')
        self.user.profile.refresh_from_db()
        self.assertTrue(bool(self.user.profile.profile_picture))

    def test_favicon_configuration(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'rel="icon" type="image/png" href="/static/images/com.png"')
        
        fav_resp = self.client.get('/favicon.ico')
        self.assertEqual(fav_resp.status_code, 301)
        self.assertEqual(fav_resp.url, '/static/images/com.png')





