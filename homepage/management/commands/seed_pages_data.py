"""
Seed content definitions for the Six Managed Content Pages:
1. School of Groups (/school-of-groups/)
2. Tell Your Story (/tell-your-story/)
3. Community Guidelines (/community-guidelines/)
4. Guidelines (/guidelines/)
5. Terms (/terms/)
6. Privacy (/privacy/)
"""

PAGES_DATA = [
    # -------------------------------------------------------------------------
    # PAGE 1: School of Groups
    # -------------------------------------------------------------------------
    {
        'slug': 'school-of-groups',
        'title': 'School of Groups',
        'badge_text': 'Peer Study Cohorts',
        'subtitle': 'Connect through structured peer cohorts, specialized tech tracks, and collaborative build groups designed to accelerate your growth in computing.',
        'summary': 'Connect through structured peer cohorts, specialized tech tracks, and collaborative build groups.',
        'status': 'published',
        'is_published': True,
        'effective_date': 'Academic Year 2024 / 2025',
        'contact_email': 'cohorts@css.community',
        'hero_cta_text': 'Explore Community Tracks',
        'hero_cta_url': '/community/',
        'sections': [
            {
                'heading': 'Welcome to School of Groups',
                'section_key': 'introduction',
                'order': 1,
                'icon_class': 'bi-compass-fill',
                'body': (
                    "<p class=\"lead mb-3\">The Computer Science Society's <strong>School of Groups</strong> is a student-powered collaborative learning architecture. It organizes computer science and engineering students into focused, domain-specific cohorts that learn, build, and ship together.</p>"
                    "<p>University computer science curricula teach strong theoretical foundations—data structures, discrete mathematics, and compiler design. However, modern software engineering requires applied toolchains: version control, distributed system design, API contracts, deployment pipelines, and collaborative code reviews. School of Groups bridges this gap by creating hands-on peer micro-communities guided by senior student mentors.</p>"
                ),
                'call_to_action_text': 'Browse Active Channels',
                'call_to_action_url': '/community/',
                'call_to_action_style': 'btn-primary',
            },
            {
                'heading': 'How School of Groups Works',
                'section_key': 'how-it-works',
                'order': 2,
                'icon_class': 'bi-diagram-3-fill',
                'body': (
                    "<p>Each cohort operates on a structured, semester-aligned cadence with four core components:</p>"
                    "<ul class=\"mb-3\">"
                    "<li><strong>Weekly Syncs:</strong> 90-minute hybrid sessions featuring code walkthroughs, architecture debates, and live debugging sessions.</li>"
                    "<li><strong>Curated Learning Roadmaps:</strong> Week-by-week roadmaps moving from foundational concepts to production deployments.</li>"
                    "<li><strong>Peer Code Reviews:</strong> Constructive reviews on GitHub pull requests where you review others' code and receive feedback on your own.</li>"
                    "<li><strong>Capstone Sprints:</strong> Multi-week team build cycles culminating in working applications submitted to CSS challenges and showcased to industry partners.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': 'Specialized Domain Tracks',
                'section_key': 'tracks',
                'order': 3,
                'icon_class': 'bi-cpu-fill',
                'body': (
                    "<p>School of Groups offers six active tracks tailored to different facets of computing:</p>"
                    "<div class=\"row g-3 mb-3\">"
                    "<div class=\"col-md-6\"><div class=\"p-3 bg-light rounded-3\"><strong>AI & Machine Learning Guild</strong><br><small class=\"text-muted\">PyTorch, computer vision, natural language processing, LLM fine-tuning, and data pipelines.</small></div></div>"
                    "<div class=\"col-md-6\"><div class=\"p-3 bg-light rounded-3\"><strong>Web & Cloud Systems Guild</strong><br><small class=\"text-muted\">Full-stack Django, React, REST/GraphQL APIs, Docker containerization, and AWS/GCP deployments.</small></div></div>"
                    "<div class=\"col-md-6\"><div class=\"p-3 bg-light rounded-3\"><strong>Cybersecurity & Ethical Hacking</strong><br><small class=\"text-muted\">CTF challenges, reverse engineering, defensive networking, cryptography, and penetration testing.</small></div></div>"
                    "<div class=\"col-md-6\"><div class=\"p-3 bg-light rounded-3\"><strong>Algorithms & Competitive Programming</strong><br><small class=\"text-muted\">ICPC problem sets, graph algorithms, dynamic programming, and technical interview preparation.</small></div></div>"
                    "<div class=\"col-md-6\"><div class=\"p-3 bg-light rounded-3\"><strong>Mobile Engineering Collective</strong><br><small class=\"text-muted\">Cross-platform Flutter, React Native, native Android/iOS tooling, and offline-first mobile databases.</small></div></div>"
                    "<div class=\"col-md-6\"><div class=\"p-3 bg-light rounded-3\"><strong>Open Source Guild</strong><br><small class=\"text-muted\">Git workflows, upstream contributions, licensing, issue triage, and building tools for campus.</small></div></div>"
                    "</div>"
                ),
            },
            {
                'heading': 'Benefits of Joining a Cohort',
                'section_key': 'benefits',
                'order': 4,
                'icon_class': 'bi-trophy-fill',
                'body': (
                    "<p>Students who participate actively in School of Groups consistently experience tangible academic and professional benefits:</p>"
                    "<ul class=\"mb-3\">"
                    "<li><strong>Accelerated Skill Acquisition:</strong> Overcome learning bottlenecks faster through peer explanations and hands-on debugging support.</li>"
                    "<li><strong>Portfolio-Ready Artifacts:</strong> Graduate beyond tutorial code by shipping publicly accessible repositories and live demo links.</li>"
                    "<li><strong>Direct Referral Pipeline:</strong> Alumni in industry regularly source internship candidates directly from cohort project showcases.</li>"
                    "<li><strong>Accountability & Camaraderie:</strong> Avoid burnout and stay consistent with peers who share your technical ambitions.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': 'Discovering & Choosing Your Track',
                'section_key': 'discovery',
                'order': 5,
                'icon_class': 'bi-search',
                'body': (
                    "<p>Whether you have never written a line of code or have built multiple web apps, there is an appropriate track for you:</p>"
                    "<p>Beginners are encouraged to join the <em>Web & Cloud Systems</em> or <em>Algorithms</em> tracks to build core fluency. Students in Year 2 and above can dive into <em>Cybersecurity</em>, <em>AI & ML</em>, or <em>Open Source</em> to build specialized domain depth.</p>"
                    "<p>You are welcome to explore multiple channel discussions before formally committing to a cohort's sprint milestones.</p>"
                ),
            },
            {
                'heading': 'Joining and Participating in Groups',
                'section_key': 'participation',
                'order': 6,
                'icon_class': 'bi-people-fill',
                'body': (
                    "<p>Joining is completely free for all enrolled students. Follow these straightforward steps to participate:</p>"
                    "<ol class=\"mb-3\">"
                    "<li>Ensure your student account is verified and profile information is complete.</li>"
                    "<li>Navigate to the <a href=\"/community/\">Community Directory</a> and select your preferred technical track.</li>"
                    "<li>Introduce yourself in the channel chat with your current year, interests, and project ideas.</li>"
                    "<li>Attend the weekly sync in Software Lab 204 or join the live hybrid stream.</li>"
                    "</ol>"
                ),
                'call_to_action_text': 'Join a Channel Discussion',
                'call_to_action_url': '/community/',
                'call_to_action_style': 'btn-outline-primary',
            },
            {
                'heading': 'Community Expectations & Commitment',
                'section_key': 'expectations',
                'order': 7,
                'icon_class': 'bi-shield-check',
                'body': (
                    "<p>Cohorts succeed when all members contribute earnestly. We uphold simple expectations:</p>"
                    "<ul class=\"mb-3\">"
                    "<li><strong>Respect and Inclusivity:</strong> Foster a psychologically safe space where no technical question is ridiculed.</li>"
                    "<li><strong>Consistency:</strong> Attend scheduled syncs and notify your cohort lead if academic deadlines require temporary absence.</li>"
                    "<li><strong>Academic Integrity:</strong> Never share homework solutions directly; teach problem-solving strategies rather than copy-pasting code.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': 'Propose a New Technical Hub or Lead a Cohort',
                'section_key': 'propose-hub',
                'order': 8,
                'icon_class': 'bi-plus-circle-fill',
                'body': (
                    "<p>Do you have a passion for a specialized domain like Game Development, Quantum Computing, or Embedded Robotics? CSS welcomes student-led track proposals!</p>"
                    "<p>Active members who have completed at least one semester can propose a new hub directly through our community portal. Provide a description, upload a square icon, and our committee will review and provision your track.</p>"
                ),
                'call_to_action_text': 'Propose a Community Hub',
                'call_to_action_url': '/community/',
                'call_to_action_style': 'btn-success',
            },
        ]
    },

    # -------------------------------------------------------------------------
    # PAGE 2: Tell Your Story
    # -------------------------------------------------------------------------
    {
        'slug': 'tell-your-story',
        'title': 'Tell Your Story',
        'badge_text': 'Speaker Series & Reflections',
        'subtitle': 'A platform for students, alumni, and peer builders to share technical triumphs, candid lessons, career journeys, and project breakthroughs.',
        'summary': 'Share your technical triumphs, candid lessons, career journeys, and project breakthroughs.',
        'status': 'published',
        'is_published': True,
        'effective_date': 'Ongoing Series',
        'contact_email': 'stories@css.community',
        'hero_cta_text': 'Read Past Stories',
        'hero_cta_url': '/blog/',
        'sections': [
            {
                'heading': 'Why Your Story Matters',
                'section_key': 'why-share',
                'order': 1,
                'icon_class': 'bi-megaphone-fill',
                'body': (
                    "<p class=\"lead mb-3\">Every engineer remembers the moment their code finally worked—and the hours of frustration that preceded it. Your journey is proof that perseverance yields mastery.</p>"
                    "<p><strong>Tell Your Story</strong> is the Computer Science Society's storytelling initiative. By documenting the challenges you faced while building a project, debugging a baffling crash, or interviewing for an internship, you create a beacon for junior students following in your footsteps.</p>"
                ),
                'call_to_action_text': 'Browse the CSS Journal',
                'call_to_action_url': '/blog/',
                'call_to_action_style': 'btn-primary',
            },
            {
                'heading': 'The Bi-Weekly Student Stage',
                'section_key': 'student-stage',
                'order': 2,
                'icon_class': 'bi-broadcast',
                'body': (
                    "<p>Every two weeks, CSS hosts an interactive hybrid student stage in the CS Building. Each session features two 15-minute student presentations followed by informal Q&A and networking.</p>"
                    "<p>The atmosphere is intentionally welcoming, supportive, and non-judgmental. It provides a safe sandbox to refine your public speaking, demonstrate live software artifacts, and practice fielding technical questions.</p>"
                ),
            },
            {
                'heading': 'Types of Stories We Welcome',
                'section_key': 'story-types',
                'order': 3,
                'icon_class': 'bi-collection-play-fill',
                'body': (
                    "<p>We celebrate diverse perspectives across all stages of the student journey:</p>"
                    "<ul class=\"mb-3\">"
                    "<li><strong>My First Project:</strong> Overcoming initial imposter syndrome and taking an idea from a blank terminal to a functioning app.</li>"
                    "<li><strong>Technical Retrospectives:</strong> Honest post-mortems of what went right, what went wrong, and what you would architect differently next time.</li>"
                    "<li><strong>Internship & Job Hunts:</strong> Preparing for technical interviews, crafting developer resumes, and navigating recruiter conversations.</li>"
                    "<li><strong>Hackathon & Open Source Sprints:</strong> Fast-paced collaborative experiences building tools under pressure.</li>"
                    "<li><strong>Research & Computing Curiosities:</strong> Deep dives into compiler design, quantum computing, or machine learning papers that sparked your curiosity.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': 'Crafting an Engaging Story: Guidelines',
                'section_key': 'writing-guide',
                'order': 4,
                'icon_class': 'bi-pencil-square',
                'body': (
                    "<p>Great technical stories focus on the <em>journey</em>, not just the finished polish. Keep these principles in mind:</p>"
                    "<ol class=\"mb-3\">"
                    "<li><strong>Frame the Problem:</strong> Why did this matter to you? What sparked the project or challenge?</li>"
                    "<li><strong>Show the Hurdles:</strong> Be transparent about the bugs, dead ends, or failed attempts you encountered.</li>"
                    "<li><strong>Explain the Solution:</strong> Walk through key architecture decisions and trade-offs made along the way.</li>"
                    "<li><strong>Summarize Takeaways:</strong> What should a reader or listener do differently based on your experience?</li>"
                    "</ol>"
                ),
            },
            {
                'heading': 'How to Submit Your Story or Pitch a Talk',
                'section_key': 'submission',
                'order': 5,
                'icon_class': 'bi-send-fill',
                'body': (
                    "<p>Ready to share your story with the society? We have two primary avenues:</p>"
                    "<ul class=\"mb-3\">"
                    "<li><strong>Write for the CSS Journal:</strong> Submit an article draft in markdown or doc format to our editorial team for publication on the blog.</li>"
                    "<li><strong>Present on the Student Stage:</strong> Email our programs committee with a 3-sentence summary of what you would like to showcase.</li>"
                    "</ul>"
                    "<p>Our editorial team provides friendly support, slide templates, and rehearsal feedback to make sure you feel confident and prepared.</p>"
                ),
                'call_to_action_text': 'Email Topic Proposal',
                'call_to_action_url': 'mailto:stories@css.community',
                'call_to_action_style': 'btn-outline-primary',
            },
            {
                'heading': 'Consent, Privacy & Media Policy',
                'section_key': 'privacy-consent',
                'order': 6,
                'icon_class': 'bi-shield-lock-fill',
                'body': (
                    "<p>We respect speaker and author autonomy:</p>"
                    "<ul class=\"mb-3\">"
                    "<li>You retain 100% intellectual property rights over your original code, presentations, and written content.</li>"
                    "<li>Student stage talks are recorded only with explicit speaker consent and can be made private upon request.</li>"
                    "<li>Personal details such as phone numbers or private email addresses are never published without authorization.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': 'Nominate a Peer Speaker',
                'section_key': 'nominate',
                'order': 7,
                'icon_class': 'bi-star-fill',
                'body': (
                    "<p>Do you know a classmate who built an impressive project or quietly navigated a tough technical challenge? Nominate them!</p>"
                    "<p>Many outstanding student developers are humble about their work. A gentle nudge or nomination from a peer often gives them the encouragement needed to share their valuable insights.</p>"
                ),
                'call_to_action_text': 'Nominate a Speaker',
                'call_to_action_url': 'mailto:stories@css.community?subject=Speaker%20Nomination',
                'call_to_action_style': 'btn-primary',
            },
        ]
    },

    # -------------------------------------------------------------------------
    # PAGE 3: Community Guidelines
    # -------------------------------------------------------------------------
    {
        'slug': 'community-guidelines',
        'title': 'Community Guidelines & Code of Conduct',
        'badge_text': 'Behavior & Safety Standards',
        'subtitle': 'Our commitments to fostering an inclusive, welcoming, and harassment-free community across all digital channels, workshops, hackathons, and labs.',
        'summary': 'Our commitments to fostering an inclusive, welcoming, and harassment-free community across all CSS spaces.',
        'status': 'published',
        'is_published': True,
        'effective_date': 'October 2024',
        'contact_email': 'ethics@css.community',
        'hero_cta_text': 'Report an Issue',
        'hero_cta_url': '#reporting-enforcement',
        'sections': [
            {
                'heading': '1. Core Values & Respectful Communication',
                'section_key': 'core-values',
                'order': 1,
                'icon_class': 'bi-heart-pulse-fill',
                'body': (
                    "<p class=\"lead mb-3\">The Computer Science Society exists to ensure every student feels supported, respected, and empowered in their computing journey.</p>"
                    "<p>We expect all members—regardless of gender identity, sexual orientation, disability, physical appearance, race, ethnicity, religion, or technical background—to treat one another with dignity, empathy, and professional courtesy.</p>"
                    "<p>Technical disagreements are normal in software engineering. Critique architectures, code implementations, and design trade-offs objectively; never attack or diminish individual contributors.</p>"
                ),
            },
            {
                'heading': '2. Zero Tolerance for Harassment & Discrimination',
                'section_key': 'anti-harassment',
                'order': 2,
                'icon_class': 'bi-shield-fill-x',
                'body': (
                    "<p>Harassment in any form will not be tolerated. Harassment includes, but is not limited to:</p>"
                    "<ul class=\"mb-3\">"
                    "<li>Offensive comments, slurs, or derogatory jokes relating to personal identity or skill level.</li>"
                    "<li>Unwelcome sexual attention, suggestive remarks, or non-consensual physical contact.</li>"
                    "<li>Deliberate intimidation, stalking, following, or harassing photography/recordings.</li>"
                    "<li>Pattern of sustained disruption of workshops, speaker presentations, or study sessions.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': '3. Hate Speech, Threats & Doxxing',
                'section_key': 'hate-speech-threats',
                'order': 3,
                'icon_class': 'bi-exclamation-octagon-fill',
                'body': (
                    "<p>CSS strictly prohibits:</p>"
                    "<ul class=\"mb-3\">"
                    "<li>Advocating for harm against individuals or groups based on protected characteristics.</li>"
                    "<li>Threats of physical violence or cyber harassment.</li>"
                    "<li>Doxxing: publishing or threatening to publish private contact numbers, physical addresses, or passwords without explicit written permission.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': '4. Spam, Promotion & Commercial Solicitations',
                'section_key': 'spam-promotion',
                'order': 4,
                'icon_class': 'bi-megaphone-fill',
                'body': (
                    "<p>To preserve high-quality signal in our channels:</p>"
                    "<ul class=\"mb-3\">"
                    "<li>Unsolicited commercial advertisements, cryptocurrency solicitations, affiliate links, and unrelated products are strictly banned.</li>"
                    "<li>Student project showcases, open-source releases, and relevant tech hackathons are warmly encouraged in designated discussion channels.</li>"
                    "<li>Do not blast identical messages across multiple channels.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': '5. Misinformation, Accuracy & Factual Technical Discourse',
                'section_key': 'misinformation',
                'order': 5,
                'icon_class': 'bi-info-circle-fill',
                'body': (
                    "<p>In our technical channels, accuracy matters. Members are expected to:</p>"
                    "<ul class=\"mb-3\">"
                    "<li>Avoid propagating unverified technical claims, security vulnerabilities, or deceptive links.</li>"
                    "<li>When quoting documentation or external stack answers, provide appropriate source citations.</li>"
                    "<li>Correct technical mistakes gracefully when peers provide counter-evidence or benchmark data.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': '6. Privacy & Personal Information Protection',
                'section_key': 'privacy-protection',
                'order': 6,
                'icon_class': 'bi-file-earmark-lock2-fill',
                'body': (
                    "<p>Respect peer privacy across all channels:</p>"
                    "<ul class=\"mb-3\">"
                    "<li>Do not take screenshots of private direct messages or confidential peer study chats to publish publicly without consent.</li>"
                    "<li>Do not scrape student email addresses or phone numbers for external mailing lists or automated campaigns.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': '7. Intellectual Property, Licensing & Academic Honesty',
                'section_key': 'ip-attribution',
                'order': 7,
                'icon_class': 'bi-patch-check-fill',
                'body': (
                    "<p>Collaboration thrives on transparency:</p>"
                    "<ul class=\"mb-3\">"
                    "<li>Always respect software licenses (MIT, Apache, GPL, BSD). Preserve original license headers when using external libraries.</li>"
                    "<li>Challenge solutions submitted for prizes or leaderboard rankings must reflect your own engineering work; cite any helper code or AI-generated scaffolding utilized.</li>"
                    "<li>Plagiarism will disqualify submissions and result in immediate review.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': '8. Appropriate Posting & Media Sharing',
                'section_key': 'appropriate-posting',
                'order': 8,
                'icon_class': 'bi-images',
                'body': (
                    "<p>All digital channels must remain safe for student environments:</p>"
                    "<ul class=\"mb-3\">"
                    "<li>Never post sexually explicit, violent, or gore media.</li>"
                    "<li>Use appropriate spoiler tags and channel topics when discussing sensitive or controversial technical subjects.</li>"
                    "<li>Keep meme sharing lighthearted and respectful; never use memes to mock or target individual community members.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': '9. Reporting Harmful Behavior & Incidents',
                'section_key': 'reporting-enforcement',
                'order': 9,
                'icon_class': 'bi-flag-fill',
                'body': (
                    "<p>If you experience or witness behavior that violates these guidelines, please notify the society leadership promptly:</p>"
                    "<p>You can contact our Ethics Committee directly at <strong>ethics@css.community</strong> or speak confidentially with any member of the Executive Committee. All reports are treated with discretion, confidentiality, and priority.</p>"
                    "<p>Please include links, screenshots, or descriptions of the incident to assist our prompt review.</p>"
                ),
                'call_to_action_text': 'Email Ethics Committee',
                'call_to_action_url': 'mailto:ethics@css.community',
                'call_to_action_style': 'btn-danger',
            },
            {
                'heading': '10. Moderation & Enforcement Procedures',
                'section_key': 'moderation-process',
                'order': 10,
                'icon_class': 'bi-gavel',
                'body': (
                    "<p>Reports are investigated impartially by the Executive Committee:</p>"
                    "<ol class=\"mb-3\">"
                    "<li><strong>Initial Assessment:</strong> Gathering facts, reviewing channel logs, and hearing all parties involved.</li>"
                    "<li><strong>Corrective Action:</strong> Depending on the severity, responses may range from private warnings and message deletion to temporary channel timeouts or permanent society expulsion.</li>"
                    "<li><strong>Formal Documentation:</strong> Key outcomes are documented in society internal logs to maintain accountability.</li>"
                    "</ol>"
                ),
            },
            {
                'heading': '11. Appeals and Review Process',
                'section_key': 'appeals',
                'order': 11,
                'icon_class': 'bi-arrow-repeat',
                'body': (
                    "<p>Any member subject to disciplinary action may submit a written appeal within 14 calendar days of notification. Appeals are reviewed by a joint panel consisting of senior executive officers and a faculty advisor to ensure fairness.</p>"
                ),
            },
        ]
    },

    # -------------------------------------------------------------------------
    # PAGE 4: Guidelines (Platform & Operational Usage)
    # -------------------------------------------------------------------------
    {
        'slug': 'guidelines',
        'title': 'Platform Guidelines & Operational Manual',
        'badge_text': 'Platform Operations',
        'subtitle': 'Practical guidance for using CSS web tools, submitting coding challenges, booking PC clinic appointments, and participating in leaderboard rankings.',
        'summary': 'Practical guidance for using CSS web tools, submitting coding challenges, and booking diagnostic appointments.',
        'status': 'published',
        'is_published': True,
        'effective_date': 'October 2024',
        'contact_email': 'support@css.community',
        'hero_cta_text': 'Browse Coding Challenges',
        'hero_cta_url': '/challenges/',
        'sections': [
            {
                'heading': '1. Getting Started on the CSS Platform',
                'section_key': 'getting-started',
                'order': 1,
                'icon_class': 'bi-door-open-fill',
                'body': (
                    "<p class=\"lead mb-3\">This platform provides the digital infrastructure supporting Computer Science Society operations—from weekly coding challenges to diagnostic hardware appointments.</p>"
                    "<p>To take full advantage of society features, register using your official university student email address. Completing your profile with your academic year, technical track, and optional GitHub handle enables custom badge tracking and leaderboard participation.</p>"
                ),
                'call_to_action_text': 'Set Up Profile',
                'call_to_action_url': '/users/profile/',
                'call_to_action_style': 'btn-primary',
            },
            {
                'heading': '2. Account Responsibilities & Credential Security',
                'section_key': 'account-security',
                'order': 2,
                'icon_class': 'bi-key-fill',
                'body': (
                    "<p>Every user is responsible for maintaining the confidentiality of their credentials:</p>"
                    "<ul class=\"mb-3\">"
                    "<li>Use a strong, unique password not shared with external websites.</li>"
                    "<li>Never share account logins or session cookies with peers.</li>"
                    "<li>The platform enforces brute-force lockout protections: after five consecutive failed attempts, accounts enter a temporary security cooldown.</li>"
                    "<li>If you suspect your credentials have been compromised, immediately reset your password via the account settings portal.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': '3. Coding Challenges & Submission Guidelines',
                'section_key': 'challenge-rules',
                'order': 3,
                'icon_class': 'bi-code-square',
                'body': (
                    "<p>Weekly coding challenges provide hands-on problem solving across web systems, algorithms, and build challenges:</p>"
                    "<ul class=\"mb-3\">"
                    "<li><strong>Public Repositories:</strong> Submit a valid, public GitHub or code repository URL starting with <code>https://</code>.</li>"
                    "<li><strong>Live Demo Links:</strong> When applicable, include a hosted demo (Vercel, Render, Fly.io, GitHub Pages).</li>"
                    "<li><strong>Implementation Writeup:</strong> Provide a concise description of your technical architecture, trade-offs, and algorithms used.</li>"
                    "<li><strong>Updates:</strong> You can edit and resubmit your solution at any time prior to the weekly deadline.</li>"
                    "</ul>"
                ),
                'call_to_action_text': 'View Active Challenges',
                'call_to_action_url': '/challenges/',
                'call_to_action_style': 'btn-outline-primary',
            },
            {
                'heading': '4. Leaderboard Ranking & Badge Integrity',
                'section_key': 'leaderboard-rules',
                'order': 4,
                'icon_class': 'bi-award-fill',
                'body': (
                    "<p>The society leaderboard showcases active challenge solvers and community contributors:</p>"
                    "<ul class=\"mb-3\">"
                    "<li>Rankings are computed from verified challenge solutions and community participation metrics.</li>"
                    "<li>Upvoting solutions is an authentic appreciation of peer work; automated upvoting, script voting, or mutual vote-ring manipulation will lead to leaderboard disqualification.</li>"
                    "<li>Users who prefer not to appear publicly on the leaderboard can toggle their visibility setting at any time in their profile.</li>"
                    "</ul>"
                ),
                'call_to_action_text': 'View Leaderboard',
                'call_to_action_url': '/leaderboard/',
                'call_to_action_style': 'btn-outline-primary',
            },
            {
                'heading': '5. Discussion Channels & Message Etiquette',
                'section_key': 'channel-etiquette',
                'order': 5,
                'icon_class': 'bi-chat-dots-fill',
                'body': (
                    "<p>Discussion channels support real-time technical queries across our guilds:</p>"
                    "<ul class=\"mb-3\">"
                    "<li>Format code snippets clearly using backticks or external pastes rather than raw wall-of-text dumps.</li>"
                    "<li>Utilize reply threads to maintain organized discussions and prevent message collision.</li>"
                    "<li>Post in the relevant channel topic (e.g., PyTorch questions belong in <code>#ai-ml</code>, Docker questions in <code>#web-cloud</code>).</li>"
                    "</ul>"
                ),
            },
            {
                'heading': '6. PC Clinic Appointments & Hardware Safety',
                'section_key': 'pc-clinic-guidelines',
                'order': 6,
                'icon_class': 'bi-tools',
                'body': (
                    "<p>The PC Clinic provides free hardware diagnostics and OS installations:</p>"
                    "<ul class=\"mb-3\">"
                    "<li><strong>Mandatory Backup:</strong> You must back up all critical academic documents and files before bringing a machine for OS re-installation or drive partitioning. CSS technicians are not liable for pre-existing drive corruption.</li>"
                    "<li><strong>Appointment Slots:</strong> Reserve your preferred time slot online. Arrive promptly at Software Lab 204 with your device and power adapter.</li>"
                    "<li><strong>Scope:</strong> Services focus on Linux dual-boot setup, toolchain installation, and diagnostic troubleshooting. We do not perform destructive component soldering or warranty voiding.</li>"
                    "</ul>"
                ),
                'call_to_action_text': 'Book Clinic Appointment',
                'call_to_action_url': '/clinic/',
                'call_to_action_style': 'btn-success',
            },
            {
                'heading': '7. Sharing Career & Internship Opportunities',
                'section_key': 'sharing-internships',
                'order': 7,
                'icon_class': 'bi-briefcase-fill',
                'body': (
                    "<p>Students and alumni can post verified career opportunities to our board:</p>"
                    "<ul class=\"mb-3\">"
                    "<li>Ensure roles are legitimate student internships, apprenticeships, or junior developer positions.</li>"
                    "<li>Provide clear company names, locations (remote/hybrid/onsite), and direct application URLs.</li>"
                    "<li>Submissions with fee-to-apply schemes or multi-level marketing traps are permanently banned.</li>"
                    "</ul>"
                ),
                'call_to_action_text': 'Explore Internships',
                'call_to_action_url': '/internships/',
                'call_to_action_style': 'btn-outline-primary',
            },
            {
                'heading': '8. Resource Conservation & API Fair Use',
                'section_key': 'fair-use',
                'order': 8,
                'icon_class': 'bi-speedometer2',
                'body': (
                    "<p>Our servers operate on university and student club cloud infrastructure:</p>"
                    "<ul class=\"mb-3\">"
                    "<li>Do not execute automated scrapers, denial-of-service scripts, or excessive poll requests against platform endpoints.</li>"
                    "<li>Respect rate limits enforced on newsletter subscription, channel messaging, and search endpoints.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': '9. Technical Support & Bug Reports',
                'section_key': 'support-bugs',
                'order': 9,
                'icon_class': 'bi-bug-fill',
                'body': (
                    "<p>Found a bug on the platform or need technical assistance with your account? We love student contributions!</p>"
                    "<p>Reach out directly to the web development team at <strong>support@css.community</strong> or file an issue on our GitHub repository.</p>"
                ),
            },
        ]
    },

    # -------------------------------------------------------------------------
    # PAGE 5: Terms of Service
    # -------------------------------------------------------------------------
    {
        'slug': 'terms',
        'title': 'Terms of Service',
        'badge_text': 'Terms & Conditions',
        'subtitle': 'The contractual agreement governing your access to and use of Computer Science Society websites, services, challenges, and facilities.',
        'summary': 'The agreement governing access to and use of Computer Science Society websites, services, challenges, and facilities.',
        'status': 'published',
        'is_published': True,
        'effective_date': 'October 15, 2024',
        'contact_email': 'governance@css.community',
        'hero_cta_text': 'Contact Governance',
        'hero_cta_url': 'mailto:governance@css.community',
        'sections': [
            {
                'heading': '1. Agreement to Terms',
                'section_key': 'agreement',
                'order': 1,
                'icon_class': 'bi-file-text-fill',
                'body': (
                    "<p class=\"lead mb-3\">By accessing or using the websites, discussion channels, diagnostic clinic services, and coding challenge portals operated by the Computer Science Society (hereinafter \"CSS\", \"we\", \"us\", or \"our\"), you agree to be bound by these Terms of Service.</p>"
                    "<p>If you do not agree with any part of these terms, you must refrain from registering an account and using our online services.</p>"
                ),
            },
            {
                'heading': '2. Eligibility and Student Status',
                'section_key': 'eligibility',
                'order': 2,
                'icon_class': 'bi-person-check-fill',
                'body': (
                    "<p>Our platforms are primarily designed for enrolled university students, alumni, and verified faculty members. By creating an account, you represent that all information provided during registration is accurate and up to date.</p>"
                ),
            },
            {
                'heading': '3. Account Security & Responsibilities',
                'section_key': 'account-security',
                'order': 3,
                'icon_class': 'bi-shield-lock-fill',
                'body': (
                    "<p>You are solely responsible for safeguarding the credentials associated with your account and for all activities conducted thereunder. You agree to notify society administrators immediately of any unauthorized access or security breach.</p>"
                ),
            },
            {
                'heading': '4. Permitted and Prohibited Conduct',
                'section_key': 'permitted-prohibited',
                'order': 4,
                'icon_class': 'bi-slash-circle-fill',
                'body': (
                    "<p>You agree to use our services exclusively for lawful educational, collaborative, and career advancement purposes. You expressly agree not to:</p>"
                    "<ul class=\"mb-3\">"
                    "<li>Attempt to probe, scan, or exploit security vulnerabilities in CSS server infrastructure.</li>"
                    "<li>Introduce viruses, worms, trojans, or automated scraping bots.</li>"
                    "<li>Impersonate other students, faculty members, or society executives.</li>"
                    "<li>Disrupt server availability through excessive traffic or denial-of-service simulations.</li>"
                    "<li>Publish copyrighted proprietary materials without authorization from rights holders.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': '5. User Content Ownership',
                'section_key': 'user-content-ownership',
                'order': 5,
                'icon_class': 'bi-code-slash',
                'body': (
                    "<p>You retain full copyright and ownership of the original software code, designs, and articles you publish on the platform or submit to coding challenges.</p>"
                ),
            },
            {
                'heading': '6. Limited License Granted to CSS',
                'section_key': 'license-to-css',
                'order': 6,
                'icon_class': 'bi-share-fill',
                'body': (
                    "<p>By submitting code solutions to public challenges or posting articles to the journal, you grant CSS a worldwide, non-exclusive, royalty-free license to display, archive, and highlight your project for non-commercial educational and promotional showcases.</p>"
                ),
            },
            {
                'heading': '7. Society Intellectual Property',
                'section_key': 'society-ip',
                'order': 7,
                'icon_class': 'bi-patch-check-fill',
                'body': (
                    "<p>The visual branding, crest, logos, platform codebase, and original curriculum materials created by CSS remain the intellectual property of the Computer Science Society and its student developers.</p>"
                ),
            },
            {
                'heading': '8. Service Availability and Modifications',
                'section_key': 'service-modifications',
                'order': 8,
                'icon_class': 'bi-gear-wide-connected',
                'body': (
                    "<p>CSS provides its platform on an \"AS IS\" and \"AS AVAILABLE\" basis. We reserve the right to modify, suspend, or discontinue any feature, endpoint, or workshop program at our discretion without prior notice.</p>"
                ),
            },
            {
                'heading': '9. Account Suspension and Termination',
                'section_key': 'termination',
                'order': 9,
                'icon_class': 'bi-x-octagon-fill',
                'body': (
                    "<p>We reserve the right to suspend or terminate accounts that breach these Terms of Service, violate Community Guidelines, or compromise system security.</p>"
                ),
            },
            {
                'heading': '10. External Links & Third-Party Services',
                'section_key': 'third-party-links',
                'order': 10,
                'icon_class': 'bi-box-arrow-up-right',
                'body': (
                    "<p>Our website links to third-party services including GitHub, external documentation, and employer application portals. CSS does not control and is not responsible for the privacy practices or content of third-party websites.</p>"
                ),
            },
            {
                'heading': '11. Limitation of Liability',
                'section_key': 'disclaimers-liability',
                'order': 11,
                'icon_class': 'bi-exclamation-triangle-fill',
                'body': (
                    "<p>To the maximum extent permitted by applicable law, CSS, its student officers, mentors, and affiliated institutions shall not be liable for any indirect, incidental, special, or consequential damages resulting from your use of or inability to access our services or hardware clinics.</p>"
                ),
            },
            {
                'heading': '12. Revisions to Terms',
                'section_key': 'revisions',
                'order': 12,
                'icon_class': 'bi-clock-history',
                'body': (
                    "<p>We may update these terms periodically to reflect new platform capabilities. Significant modifications will be communicated through platform announcement banners. Continued usage constitutes acceptance of updated terms.</p>"
                ),
            },
            {
                'heading': '13. Governance & Inquiries',
                'section_key': 'governance-contact',
                'order': 13,
                'icon_class': 'bi-envelope-at-fill',
                'body': (
                    "<p>These terms shall be interpreted in accordance with university student society regulations and applicable territorial guidelines.</p>"
                    "<p>For legal, compliance, or governance questions, please contact our committee at <strong>governance@css.community</strong>.</p>"
                ),
                'call_to_action_text': 'Email Governance Team',
                'call_to_action_url': 'mailto:governance@css.community',
                'call_to_action_style': 'btn-outline-primary',
            },
        ]
    },

    # -------------------------------------------------------------------------
    # PAGE 6: Privacy Policy
    # -------------------------------------------------------------------------
    {
        'slug': 'privacy',
        'title': 'Privacy Policy',
        'badge_text': 'Data Protection & Transparency',
        'subtitle': 'An honest and detailed explanation of how the Computer Science Society collects, handles, stores, and protects student personal information.',
        'summary': 'An honest and detailed explanation of how CSS handles and protects student personal information.',
        'status': 'published',
        'is_published': True,
        'effective_date': 'October 15, 2024',
        'contact_email': 'privacy@css.community',
        'hero_cta_text': 'Privacy Inquiries',
        'hero_cta_url': 'mailto:privacy@css.community',
        'sections': [
            {
                'heading': '1. Introduction & Scope',
                'section_key': 'scope',
                'order': 1,
                'icon_class': 'bi-shield-check',
                'body': (
                    "<p class=\"lead mb-3\">The Computer Science Society (\"CSS\", \"we\") takes your digital privacy seriously. This Privacy Policy details our data collection and protection practices across our website, clinic appointment system, and discussion channels.</p>"
                    "<p>Our guiding philosophy is simple: we collect only what is strictly necessary to deliver student society services, verify academic affiliation, and maintain platform security.</p>"
                ),
            },
            {
                'heading': '2. Categories of Information Collected',
                'section_key': 'information-collected',
                'order': 2,
                'icon_class': 'bi-card-list',
                'body': (
                    "<p>We collect information across three specific contexts:</p>"
                    "<ul class=\"mb-3\">"
                    "<li><strong>Account Registration:</strong> Username, student email address, first and last name, academic year, department, and password (hashed).</li>"
                    "<li><strong>Profile & Participation Data:</strong> Optional profile picture, GitHub URL, challenge solutions, channel discussion posts, and solution upvotes.</li>"
                    "<li><strong>Diagnostic Service Requests:</strong> Device brand, model, and issue description provided when booking a PC Clinic appointment.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': '3. Information Collected Automatically',
                'section_key': 'automated-data',
                'order': 3,
                'icon_class': 'bi-hdd-network-fill',
                'body': (
                    "<p>When you navigate our web portal, our servers record standard technical telemetry:</p>"
                    "<ul class=\"mb-3\">"
                    "<li>Internet Protocol (IP) addresses used for brute-force rate limiting and security lockout defense.</li>"
                    "<li>Browser user-agent strings and timestamp data recorded in system diagnostic logs.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': '4. Purposes of Data Processing',
                'section_key': 'purposes-processing',
                'order': 4,
                'icon_class': 'bi-check2-all',
                'body': (
                    "<p>Your information is processed strictly for legitimate society operations:</p>"
                    "<ul class=\"mb-3\">"
                    "<li>Authenticating your session and verifying student status.</li>"
                    "<li>Managing challenge submissions and compiling the leaderboard.</li>"
                    "<li>Scheduling technician resources for PC Clinic reservations.</li>"
                    "<li>Delivering society announcements and weekly newsletter digests (with one-click unsubscribe).</li>"
                    "</ul>"
                ),
            },
            {
                'heading': '5. Storage, Encryption & Security Protections',
                'section_key': 'storage-security',
                'order': 5,
                'icon_class': 'bi-lock-fill',
                'body': (
                    "<p>We implement defense-in-depth security measures:</p>"
                    "<ul class=\"mb-3\">"
                    "<li><strong>Encryption in Transit:</strong> All web traffic is strictly served over modern TLS/HTTPS encryption with HTTP Strict Transport Security (HSTS).</li>"
                    "<li><strong>Password Hashing:</strong> Passwords are never stored in plaintext; they are securely hashed using salted PBKDF2 with SHA-256 (1,000,000 iterations).</li>"
                    "<li><strong>Restricted Access:</strong> Database records are accessible only by authorized administrative credentials.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': '6. Sharing and Disclosure Policy',
                'section_key': 'sharing-disclosure',
                'order': 6,
                'icon_class': 'bi-shield-x',
                'body': (
                    "<div class=\"alert alert-success border-0 mb-3\"><i class=\"bi bi-check-circle-fill me-2\"></i><strong>Our Commercial Pledge:</strong> We do not sell, rent, monetize, or trade your personal data to commercial advertising brokers or data brokers under any circumstances.</div>"
                    "<p>Information is disclosed only under legal obligations or when explicitly consented to (such as when you share your resume with internship partners).</p>"
                ),
            },
            {
                'heading': '7. Cookies and Local Session Storage',
                'section_key': 'cookies',
                'order': 7,
                'icon_class': 'bi-cookie',
                'body': (
                    "<p>Our website utilizes strictly essential session cookies:</p>"
                    "<ul class=\"mb-3\">"
                    "<li><strong>Session Cookie (<code>sessionid</code>):</strong> Keeps you logged in as you navigate between pages.</li>"
                    "<li><strong>CSRF Cookie (<code>csrftoken</code>):</strong> Protects forms against Cross-Site Request Forgery attacks.</li>"
                    "</ul>"
                    "<p>We do not use third-party tracking pixels, advertising cookies, or behavioral trackers.</p>"
                ),
            },
            {
                'heading': '8. Data Retention and Account Deletion',
                'section_key': 'retention-deletion',
                'order': 8,
                'icon_class': 'bi-trash-fill',
                'body': (
                    "<p>We retain your profile data during your active participation in society activities.</p>"
                    "<p>You have full autonomy over your account. You can deactivate your account directly in <a href=\"/users/settings/\">Account Settings</a>, which immediately terminates your sessions and anonymizes your profile. To request full database purging, contact <strong>privacy@css.community</strong>.</p>"
                ),
            },
            {
                'heading': '9. Your Privacy Rights and Data Controls',
                'section_key': 'user-rights',
                'order': 9,
                'icon_class': 'bi-person-gear',
                'body': (
                    "<p>You hold the right to:</p>"
                    "<ul class=\"mb-3\">"
                    "<li>Inspect the personal information held about you in our systems.</li>"
                    "<li>Correct inaccurate profile details via your settings dashboard.</li>"
                    "<li>Opt out of the public society leaderboard while retaining full challenge submission privileges.</li>"
                    "<li>Unsubscribe from society emails at any time.</li>"
                    "</ul>"
                ),
            },
            {
                'heading': '10. Children and Minors',
                'section_key': 'minors',
                'order': 10,
                'icon_class': 'bi-person-badge',
                'body': (
                    "<p>Our platform is designed for tertiary university students and adult learners. We do not knowingly collect personal information from individuals under 16 years of age.</p>"
                ),
            },
            {
                'heading': '11. Privacy Inquiries and Data Requests',
                'section_key': 'privacy-contact',
                'order': 11,
                'icon_class': 'bi-envelope-check-fill',
                'body': (
                    "<p>For privacy questions, data export requests, or erasure requests, reach out directly to our designated student privacy contact:</p>"
                    "<p>Email: <strong>privacy@css.community</strong></p>"
                    "<p>We endeavor to respond to all student privacy inquiries within three business days.</p>"
                ),
                'call_to_action_text': 'Submit Privacy Inquiry',
                'call_to_action_url': 'mailto:privacy@css.community',
                'call_to_action_style': 'btn-outline-primary',
            },
        ]
    },
]

