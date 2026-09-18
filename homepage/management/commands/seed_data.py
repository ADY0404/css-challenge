from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from homepage.models import (
    Challenge,
    ChallengeSubmission,
    Article,
    Internship,
    CommunityMessage,
    ClinicSession,
    InfoPage,
    CommunityChannel,
    SiteConfiguration,
)
from activities.models import Event, GuestSpeaker
from executives.models import Executive
from users.models import Profile
from datetime import date, time, timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Seeds initial realistic data for challenges, articles, internships, events, and executives'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # 1. Ensure test demo user exists
        demo_user, created = User.objects.get_or_create(
            username='student_dev',
            defaults={
                'first_name': 'Alex',
                'last_name': 'Okonkwo',
                'email': 'alex.okonkwo@student.university.edu',
                'is_staff': False,
            }
        )
        if created:
            demo_user.set_password('studentpass123')
            demo_user.save()
        
        profile, _ = Profile.objects.get_or_create(user=demo_user)
        profile.year = 3
        profile.department = 'Computer Science'
        profile.bio = 'Junior CS major focused on backend systems, distributed computing, and open source.'
        profile.github_url = 'https://github.com'
        profile.save()

        # 2. Seed Challenges
        challenges_data = [
            {
                'title': 'Design a better campus connection',
                'slug': 'design-a-better-campus-connection',
                'category': 'Design & Dev',
                'difficulty': 'Beginner',
                'week_label': 'Week 04',
                'deadline_text': 'Submit by Sunday · 11:59 PM',
                'icon_class': 'bi-people-fill',
                'art_class': 'main-challenge-art',
                'is_featured': True,
                'summary': 'Create a simple digital experience that helps students find study partners, faculty hours, or tech societies on campus.',
                'description': (
                    "Campus life can feel fragmented when resources and peer groups are scattered across Discord, WhatsApp, and notice boards. "
                    "In this challenge, design and implement a single cohesive interface—either a responsive web page or a lightweight prototype—"
                    "that helps university students discover peers with complementary skills, join study tracks, or find upcoming campus tech workshops."
                ),
                'requirements': (
                    "1. Provide a responsive layout (desktop and mobile viewport friendly).\n"
                    "2. Include at least 3 distinct category filters or search mechanisms.\n"
                    "3. Include a functional call-to-action (e.g., student RSVP or bookmark feature).\n"
                    "4. Submit your source code via GitHub and optionally provide a deployed URL."
                ),
            },
            {
                'title': 'Reimagine your student dashboard',
                'slug': 'reimagine-your-student-dashboard',
                'category': 'Build Log',
                'difficulty': 'Intermediate',
                'week_label': 'Week 03',
                'deadline_text': 'Open Challenge',
                'icon_class': 'bi-window-stack',
                'art_class': 'art-purple',
                'is_featured': False,
                'summary': 'Make an everyday university dashboard task feel 10x clearer, faster, and more intuitive for your peers.',
                'description': (
                    "University portals often suffer from cumbersome navigation and cluttered tables. "
                    "Re-architect a student course portal view: focus on quick timetable access, GPA tracking, assignment countdowns, "
                    "and clean typographic hierarchy."
                ),
                'requirements': (
                    "1. Clean accessible UI adhering to WCAG color contrast standards.\n"
                    "2. Support dynamic state (e.g. toggling completed course milestones).\n"
                    "3. Document your design trade-offs in a README.md file."
                ),
            },
            {
                'title': 'Tell a useful tech story',
                'slug': 'tell-a-useful-tech-story',
                'category': 'Community',
                'difficulty': 'Beginner',
                'week_label': 'Week 02',
                'deadline_text': 'Open Challenge',
                'icon_class': 'bi-chat-square-text',
                'art_class': 'art-teal',
                'is_featured': False,
                'summary': 'Turn something tricky you learned recently into a crystal-clear, beautifully illustrated explainer post.',
                'description': (
                    "Communication is one of the most critical engineering skills. Write and code a visual, interactive tutorial "
                    "explaining an algorithmic concept (such as Big-O notation, Git rebase vs merge, or how HTTP headers work) in plain English."
                ),
                'requirements': (
                    "1. Maximum 1,000 words with clear code examples.\n"
                    "2. Include at least one custom diagram, interactive chart, or ASCII illustration.\n"
                    "3. Provide practical analogies suitable for first-year CS students."
                ),
            },
            {
                'title': 'Find a pattern that matters',
                'slug': 'find-a-pattern-that-matters',
                'category': 'Data Science',
                'difficulty': 'Intermediate',
                'week_label': 'Week 01',
                'deadline_text': 'Open Challenge',
                'icon_class': 'bi-bar-chart-line',
                'art_class': 'art-gold',
                'is_featured': False,
                'summary': 'Use an open dataset to uncover, visualize, and explain one impactful insight with Python or SQL.',
                'description': (
                    "Analyze a public dataset (e.g. campus energy usage, public transit schedules, or tech salary trends). "
                    "Clean the data, compute summary metrics, and craft an insightful visualization with a 3-paragraph summary of your findings."
                ),
                'requirements': (
                    "1. Submit a reproducible Jupyter notebook or Python script.\n"
                    "2. Include data cleaning notes (handling missing values, data types).\n"
                    "3. Present at least 2 clear charts with labeled axes and legends."
                ),
            },
        ]

        for cdata in challenges_data:
            c, _ = Challenge.objects.update_or_create(slug=cdata['slug'], defaults=cdata)
        self.stdout.write(f"  Loaded {len(challenges_data)} Challenges.")

        # Seed 1 initial submission for the featured challenge
        featured_challenge = Challenge.objects.get(slug='design-a-better-campus-connection')
        ChallengeSubmission.objects.get_or_create(
            challenge=featured_challenge,
            user=demo_user,
            defaults={
                'project_title': 'CampusHub - Peer Study Matcher',
                'repo_url': 'https://github.com/alex-dev/campushub-project',
                'demo_url': 'https://campushub-demo.vercel.app',
                'description': 'Built with HTML5, Bootstrap 5, and vanilla JS. Features instant track filtering and mobile card interactions.',
            }
        )

        # 3. Seed Articles (Blog)
        articles_data = [
            {
                'title': 'The effect of AI on humanity starts with the questions we ask.',
                'slug': 'the-effect-of-ai-on-humanity',
                'category': 'learning',
                'author_name': 'Oluwaseun Adebayo',
                'author_role': 'CSS Editorial Team',
                'read_time': '6 min read',
                'is_featured': True,
                'image_path': 'images/AI.jpeg',
                'summary': 'AI is changing how we learn, create, and work. Here is how our community is making space for the thoughtful, human side of the conversation.',
                'content': (
                    "Artificial intelligence is no longer an abstract academic theory confined to research laboratories; "
                    "it is now a daily tool in how students write code, draft essays, and debug complex software architectures.\n\n"
                    "Yet as generative models and autonomous agents become ubiquitous, the most important engineering skill is shifting: "
                    "it is no longer just about generating syntax, but about having the critical judgment to evaluate correctness, "
                    "security, and ethical consequences.\n\n"
                    "The Human Component in Software Engineering\n\n"
                    "When we prompt an AI assistant to write a database query or scaffold a React component, we are making assumptions about "
                    "performance, data ownership, and edge cases. In the Computer Science Society, we emphasize that technical mastery begins "
                    "with understanding the fundamentals: data structures, algorithmic complexity, and systems design.\n\n"
                    "How We Are Responding\n\n"
                    "Through our AI Study Jams and School of Groups cohorts, we encourage students to inspect model weights, understand attention "
                    "mechanisms, and explore responsible AI deployment. Join us every alternate Thursday as we dissect modern AI papers and "
                    "build ethical, human-centric software."
                ),
            },
            {
                'title': "From blank page to working project: a beginner's map",
                'slug': 'from-blank-page-to-working-project',
                'category': 'build',
                'author_name': 'Chioma Eze',
                'author_role': 'CSS Mentor & Alum',
                'read_time': '4 min read',
                'is_featured': False,
                'image_path': 'images/gat.jpeg',
                'summary': 'Small steps and a few good habits can get any technical project moving from an intimidating idea to working code.',
                'content': (
                    "Every experienced engineer knows the feeling of staring at an empty code editor. "
                    "When building your first independent project, the scope often feels overwhelming.\n\n"
                    "1. Narrow the Problem Statement\n\n"
                    "The single biggest reason student projects remain unfinished is scope creep. Instead of building 'a social network for developers', "
                    "build a tool that lets two students share code snippets with syntax highlighting. Solve one real problem completely before adding features.\n\n"
                    "2. Write the README First\n\n"
                    "Before writing a line of code, draft your documentation. What does the app do? What are the three primary endpoints or user actions? "
                    "This acts as your architectural roadmap.\n\n"
                    "3. Commit Daily, Even Small Diffs\n\n"
                    "Consistent small commits build momentum. A functional milestone completed today is better than an over-engineered architecture tomorrow."
                ),
            },
            {
                'title': 'What happened when we gave freshers the mic',
                'slug': 'what-happened-when-freshers-took-the-mic',
                'category': 'community',
                'author_name': 'Ibrahim Musa',
                'author_role': 'Student Community Lead',
                'read_time': '3 min read',
                'is_featured': False,
                'image_path': 'images/bot.jpeg',
                'summary': 'Five memorable insights and creative project concepts that emerged from our latest orientation lightning talks.',
                'content': (
                    "During our annual CSS Freshers' Orientation, we set aside traditional executive speeches and gave first-year students 3 minutes each "
                    "to pitch a software idea they dreamed of building.\n\n"
                    "From an automated campus shuttle tracker to a localized peer tutoring queue, the creativity in the room was electric. "
                    "Several of these ideas have now transitioned into active collaborative projects within the CSS School of Groups.\n\n"
                    "Our community succeeds when beginners feel empowered to contribute on day one."
                ),
            },
            {
                'title': 'Your first tech role is closer than it feels',
                'slug': 'your-first-tech-role-is-closer-than-it-feels',
                'category': 'career',
                'author_name': 'Amina Yusuf',
                'author_role': 'Graduate Software Engineer',
                'read_time': '5 min read',
                'is_featured': False,
                'image_path': 'images/AI.jpeg',
                'summary': 'A practical guide to cultivating technical confidence, polishing your portfolio, and approaching your first interviews.',
                'content': (
                    "Technical imposter syndrome is real, especially when scanning job postings that demand five years of experience for entry-level roles. "
                    "However, hiring teams look for specific indicators of potential: genuine curiosity, git literacy, problem-solving methodology, and communication.\n\n"
                    "Focus on building 2 solid projects where you can explain every architectural decision, rather than 10 cloned tutorials. "
                    "Take advantage of the CSS Internships board and attend our upcoming mock interview sprint!"
                ),
            },
        ]

        for adata in articles_data:
            Article.objects.update_or_create(slug=adata['slug'], defaults=adata)
        self.stdout.write(f"  Loaded {len(articles_data)} Articles.")

        # 4. Seed Internships
        internships_data = [
            {
                'title': 'Software Engineering Intern',
                'company': 'Nexa Systems',
                'location': 'Lagos, Nigeria · Hybrid',
                'role_type': 'Internship',
                'duration': '12 weeks',
                'is_featured': True,
                'tags': 'Python, React, PostgreSQL, Docker',
                'apply_url': 'https://careers.example.com/nexa-swe',
                'description': (
                    "Help build tools that make everyday finance feel simpler and more reliable. "
                    "You will work closely with product and engineering teams on production features used by thousands of users across West Africa."
                ),
                'requirements': (
                    "• Strong foundational knowledge of Python and modern JavaScript.\n"
                    "• Understanding of RESTful APIs, HTTP protocols, and relational databases.\n"
                    "• Familiarity with Git version control and collaborative workflows.\n"
                    "• Enrolled in an undergraduate Computer Science or related degree program."
                ),
            },
            {
                'title': 'Product Design Intern',
                'company': 'Kora Studio',
                'location': 'Remote',
                'role_type': 'Internship',
                'duration': '10 weeks',
                'is_featured': False,
                'tags': 'Figma, User Research, Wireframing, Design Systems',
                'apply_url': 'https://careers.example.com/kora-design',
                'description': (
                    "Collaborate with lead designers to create intuitive, accessible user experiences for web and mobile platforms. "
                    "You will conduct user interviews, iterate on design tokens, and build high-fidelity interactive prototypes."
                ),
                'requirements': (
                    "• Proficiency with Figma, auto-layout, and prototyping tools.\n"
                    "• An online portfolio showcasing at least one UX case study.\n"
                    "• Passion for inclusive, accessible interface design."
                ),
            },
            {
                'title': 'Data Analyst Intern',
                'company': 'Clearview Health',
                'location': 'Abuja, Nigeria · On-site',
                'role_type': 'Internship',
                'duration': '12 weeks',
                'is_featured': False,
                'tags': 'SQL, Python, Pandas, Tableau',
                'apply_url': 'https://careers.example.com/clearview-data',
                'description': (
                    "Analyze healthcare service utilization data to assist clinicians and health administrators in making data-backed operational decisions."
                ),
                'requirements': (
                    "• Working knowledge of SQL (joins, aggregations, window functions).\n"
                    "• Experience with data visualization libraries (Seaborn, Matplotlib, or Tableau).\n"
                    "• Strong attention to detail and data integrity."
                ),
            },
        ]

        for idata in internships_data:
            Internship.objects.update_or_create(
                title=idata['title'],
                company=idata['company'],
                defaults=idata
            )
        self.stdout.write(f"  Loaded {len(internships_data)} Internships.")

        # 5. Seed Events & Guest Speakers
        today = timezone.now().date()
        events_data = [
            {
                'title': 'CSS Freshers Orientation & Tech Induction',
                'date': today + timedelta(days=5),
                'time': time(10, 0),
                'description': 'Welcome to the Computer Science Society! Meet faculty advisers, discover specialized technical tracks, and network with senior peer mentors.',
                'activity': 'Keynote on navigating university CS, interactive track breakout sessions, hardware clinic walkthrough, and Q&A.',
                'image': 'activities/gat.jpeg',
                'banner_image': 'events/images/gat.jpeg',
                'button_text': 'View Event',
                'speakers': [
                    {'name': 'Dr. K. Mensah', 'title': 'Head of Computer Science Dept', 'image_url': 'guest_speakers/man1.jpg'},
                    {'name': 'Tobi Oladipo', 'title': 'CSS Society President', 'image_url': 'guest_speakers/man2.jpg'},
                ]
            },
            {
                'title': 'Fullstack Web Workshop: Django & React Workflows',
                'date': today + timedelta(days=12),
                'time': time(14, 0),
                'description': 'Hands-on coding workshop building modern web APIs with Django REST Framework and consuming them in React with real-time UI updates.',
                'activity': 'Live code-along, Git branching exercises, authentication implementation, and deployment on cloud infrastructure.',
                'image': 'activities/bot.jpeg',
                'banner_image': 'events/images/bot.jpeg',
                'button_text': 'View Event',
                'speakers': [
                    {'name': 'Zainab Adeleke', 'title': 'CSS Director of Software & Projects', 'image_url': 'guest_speakers/man3.jpg'},
                ]
            },
            {
                'title': 'AI Study Jam: Practical Machine Learning with PyTorch',
                'date': today + timedelta(days=19),
                'time': time(11, 0),
                'description': 'Introduction to tensors, neural network architectures, and training custom computer vision models with PyTorch.',
                'activity': 'Interactive Google Colab walkthrough, loss optimization analysis, and hands-on image classification sprint.',
                'image': 'activities/AI.jpeg',
                'banner_image': 'events/images/AI.jpeg',
                'button_text': 'View Event',
                'speakers': [
                    {'name': 'David Adeleke', 'title': 'AI Research Fellow', 'image_url': 'guest_speakers/man4.jpg'},
                ]
            },
        ]

        for edata in events_data:
            speakers = edata.pop('speakers')
            event, _ = Event.objects.update_or_create(
                title=edata['title'],
                defaults=edata
            )
            for sdata in speakers:
                GuestSpeaker.objects.get_or_create(
                    event=event,
                    name=sdata['name'],
                    defaults=sdata
                )
        self.stdout.write(f"  Loaded {len(events_data)} Events with Guest Speakers.")

        # 6. Seed Executives for 2024/25 session
        executives_data = [
            {'name': 'Tobi Oladipo', 'position': 'President', 'academic_year': '2024/25', 'image': 'events/images/man1.jpg'},
            {'name': 'Aisha Bello', 'position': 'Vice President', 'academic_year': '2024/25', 'image': 'events/images/man2.jpg'},
            {'name': 'Emmanuel Nwosu', 'position': 'General Secretary', 'academic_year': '2024/25', 'image': 'events/images/man3.jpg'},
            {'name': 'Zainab Adeleke', 'position': 'Director of Software & Projects', 'academic_year': '2024/25', 'image': 'events/images/man4.jpg'},
            {'name': 'Kevin Mensah', 'position': 'Director of Academic Affairs', 'academic_year': '2024/25', 'image': 'events/images/man5.jpg'},
            {'name': 'Praise Okafor', 'position': 'Public Relations Officer', 'academic_year': '2024/25', 'image': 'events/images/man6.jpg'},
        ]

        for exdata in executives_data:
            Executive.objects.update_or_create(
                name=exdata['name'],
                academic_year=exdata['academic_year'],
                defaults=exdata
            )
        self.stdout.write(f"  Loaded {len(executives_data)} Executives for 2024/25.")

        # 7. Seed Initial Community Messages
        community_messages = [
            {'channel': 'ai-ml', 'user': demo_user, 'text': 'Welcome to the AI & Machine Learning Hub! What model architectures are you exploring this semester?'},
            {'channel': 'web-cloud', 'user': demo_user, 'text': 'Hey everyone! We are prepping the starter template for the upcoming Fullstack workshop.'},
            {'channel': 'cybersecurity', 'user': demo_user, 'text': 'CTF team registration is open for next weekend. Let us know if you want to join the squad!'},
        ]
        for msg in community_messages:
            CommunityMessage.objects.get_or_create(
                channel=msg['channel'],
                user=msg['user'],
                text=msg['text']
            )
        self.stdout.write("  Loaded initial community messages.")

        # 8. Seed Clinic Sessions
        clinic_sessions = [
            {
                'session_code': '2024-10-04',
                'date_title': 'Wednesday, Oct 4, 2024',
                'time_slot': '2:00 PM – 5:30 PM',
                'venue': 'Software Lab 204, CS Building',
                'focus_topic': 'Linux Dual-Boot & OS Installation (Ubuntu 24.04 LTS / Fedora 40)',
                'capacity': 12,
                'leads': 'David Koomson & Zainab Adeleke',
                'badge_text': 'Next Upcoming Session',
                'is_active': True,
                'order': 1,
            },
            {
                'session_code': '2024-10-06',
                'date_title': 'Friday, Oct 6, 2024',
                'time_slot': '2:00 PM – 6:00 PM',
                'venue': 'Software Lab 204, CS Building',
                'focus_topic': 'Dev Environments: Docker, Git, VS Code, Python & C++ Toolchains',
                'capacity': 12,
                'leads': 'Kevin Mensah & Alex Okonkwo',
                'badge_text': 'Popular Session',
                'is_active': True,
                'order': 2,
            },
            {
                'session_code': '2024-10-11',
                'date_title': 'Wednesday, Oct 11, 2024',
                'time_slot': '2:00 PM – 5:30 PM',
                'venue': 'Software Lab 204, CS Building',
                'focus_topic': 'Hardware Diagnostics, Thermal Repasting & Fan Deep Cleaning',
                'capacity': 10,
                'leads': 'Emmanuel Nwosu & Hardware SIG',
                'badge_text': '',
                'is_active': True,
                'order': 3,
            },
            {
                'session_code': '2024-10-13',
                'date_title': 'Friday, Oct 13, 2024',
                'time_slot': '2:00 PM – 6:00 PM',
                'venue': 'Software Lab 204, CS Building',
                'focus_topic': 'Malware Removal, Storage Optimization & Security Hardening',
                'capacity': 12,
                'leads': 'Cybersecurity SIG Volunteers',
                'badge_text': '',
                'is_active': True,
                'order': 4,
            },
            {
                'session_code': '2024-10-18',
                'date_title': 'Wednesday, Oct 18, 2024',
                'time_slot': '2:00 PM – 5:30 PM',
                'venue': 'Software Lab 204, CS Building',
                'focus_topic': 'Mid-Semester General Triage, Driver Troubleshooting & OS Recovery',
                'capacity': 14,
                'leads': 'All Clinic Technicians',
                'badge_text': '',
                'is_active': True,
                'order': 5,
            },
        ]
        for cs in clinic_sessions:
            ClinicSession.objects.update_or_create(
                session_code=cs['session_code'],
                defaults=cs
            )
        self.stdout.write(f"  Loaded {len(clinic_sessions)} Clinic Sessions.")

        # 9. Seed Informational / Policy Pages
        info_pages = [
            {
                'slug': 'guidelines',
                'title': 'Society Guidelines',
                'summary': 'Be respectful, inclusive, and constructive. These principles help keep CSS a welcoming place to learn and collaborate.',
                'body': 'These community guidelines outline expected behavior, respect for shared resources, academic honesty, and inclusive participation across all Computer Science Society forums, workshops, hackathons, and collaborative tracks.',
            },
            {
                'slug': 'programs',
                'title': 'CSS Programs',
                'summary': 'Explore society programs including School of Groups, Tell Your Story, PC Clinic, and Hackathons.',
                'body': 'CSS provides academic and career advancement opportunities through specialized cohorts, peer mentorship, hands-on clinics, and annual software competitions designed to accelerate your growth as an engineer.',
            },
            {
                'slug': 'terms',
                'title': 'Terms of Use',
                'summary': 'Use CSS community spaces responsibly and respect the privacy, work, and time of other members.',
                'body': 'By registering an account and accessing CSS web services, coding challenge submissions, or community channels, members agree to adhere to university acceptable use policies, code confidentiality, and respectful conduct.',
            },
            {
                'slug': 'privacy',
                'title': 'Privacy Policy',
                'summary': 'CSS uses the information you provide to operate your account and deliver society activities.',
                'body': 'We respect your student data privacy. Information collected during account registration, event RSVPs, or PC Clinic reservations is strictly used for university society operations and is never shared with unauthorized third parties.',
            },
        ]
        for ip in info_pages:
            InfoPage.objects.update_or_create(
                slug=ip['slug'],
                defaults=ip
            )
        self.stdout.write(f"  Loaded {len(info_pages)} Informational CMS Pages.")

        # 10. Seed Community Channels
        channels_data = [
            {
                'slug': 'ai-ml',
                'name': 'Future of AI & Machine Learning',
                'category': 'AI & Data Systems',
                'description': 'Deep learning study groups, computer vision, transformer models, and AI research discussions.',
                'icon_class': 'bi-cpu-fill',
                'accent_color': '#4F46E5',
                'accent_bg': '#EEF2FF',
                'rail_class': 'rail-ai',
                'order': 1,
            },
            {
                'slug': 'web-cloud',
                'name': 'Web & Cloud Systems Guild',
                'category': 'Web & Infrastructure',
                'description': 'Frontend frameworks, distributed backends, REST/GraphQL APIs, Docker, and AWS/GCP deployments.',
                'icon_class': 'bi-cloud-arrow-up-fill',
                'accent_color': '#059669',
                'accent_bg': '#ECFDF5',
                'rail_class': 'rail-web',
                'order': 2,
            },
            {
                'slug': 'cybersecurity',
                'name': 'Cybersecurity & Ethical Hacking',
                'category': 'Systems Security',
                'description': 'Capture The Flag (CTF) competitions, network forensics, reverse engineering, and threat modeling.',
                'icon_class': 'bi-shield-lock-fill',
                'accent_color': '#DC2626',
                'accent_bg': '#FEF2F2',
                'rail_class': 'rail-sec',
                'order': 3,
            },
            {
                'slug': 'algorithms',
                'name': 'Competitive Programming & Algorithms',
                'category': 'Problem Solving',
                'description': 'Data structures, algorithm complexity, dynamic programming, and ICPC contest preparation.',
                'icon_class': 'bi-diagram-3-fill',
                'accent_color': '#D97706',
                'accent_bg': '#FFFBEB',
                'rail_class': 'rail-algo',
                'order': 4,
            },
            {
                'slug': 'mobile',
                'name': 'Mobile Apps & Engineering',
                'category': 'Mobile Ecosystems',
                'description': 'Flutter, React Native, iOS Swift, and Android Jetpack Compose production apps and tooling.',
                'icon_class': 'bi-phone-fill',
                'accent_color': '#0284C7',
                'accent_bg': '#F0F9FF',
                'rail_class': 'rail-mobile',
                'order': 5,
            },
            {
                'slug': 'open-source',
                'name': 'Open Source Collective',
                'category': 'Community Engineering',
                'description': 'Contributing to GitHub projects, society web tools, git collaboration, and community packages.',
                'icon_class': 'bi-git',
                'accent_color': '#475569',
                'accent_bg': '#F1F5F9',
                'rail_class': 'rail-oss',
                'order': 6,
            },
        ]
        for ch in channels_data:
            CommunityChannel.objects.update_or_create(
                slug=ch['slug'],
                defaults=ch
            )
        self.stdout.write(f"  Loaded {len(channels_data)} Community Channels.")

        # 11. Seed Site Configuration Singleton
        site_config = SiteConfiguration.get_solo()
        site_config.save()
        self.stdout.write("  Ensured SiteConfiguration singleton is initialized.")

        self.stdout.write(self.style.SUCCESS("Successfully seeded all database tables!"))

