"""
Custom Admin Site organization and dashboard enhancements.
Groups all models into clear, intuitive operational categories instead of raw app dumps.
"""


def setup_custom_admin_dashboard(site):
    """
    Configure organized model groupings on the given AdminSite instance.
    """
    orig_get_app_list = site.get_app_list

    def custom_get_app_list(request, app_label=None):
        raw_apps = orig_get_app_list(request, app_label)
        if app_label:
            return raw_apps

        # Map every model by its object_name
        all_models = {}
        for app in raw_apps:
            for model in app.get('models', []):
                all_models[model['object_name']] = model

        sections_def = [
            (
                'Site Governance & Security',
                'governance',
                ['SiteConfiguration', 'User', 'Profile', 'Group', 'InfoPage'],
            ),
            (
                'Coding Challenges & Leaderboard',
                'challenges',
                ['Challenge', 'ChallengeSubmission', 'SubmissionUpvote'],
            ),
            (
                'Community Channels & Discussions',
                'community',
                ['CommunityChannel', 'CommunityMessage'],
            ),
            (
                'Activities, Events & Programs',
                'activities',
                ['Event', 'EventRegistration', 'GuestSpeaker', 'Program', 'Executive', 'SocialMedia'],
            ),
            (
                'Career, Clinic & Student Support',
                'opportunities',
                ['Internship', 'ClinicSession', 'ClinicAppointment', 'Article', 'NewsletterSubscriber'],
            ),
        ]

        new_app_list = []
        used_models = set()

        for section_name, section_label, model_names in sections_def:
            section_models = []
            for mname in model_names:
                if mname in all_models:
                    section_models.append(all_models[mname])
                    used_models.add(mname)

            if section_models:
                new_app_list.append({
                    'name': section_name,
                    'app_label': section_label,
                    'app_url': section_models[0].get('admin_url', '#'),
                    'has_module_perms': True,
                    'models': section_models,
                })

        # Capture any unlisted models to ensure full forward-compatibility
        remaining = [m for mname, m in all_models.items() if mname not in used_models]
        if remaining:
            new_app_list.append({
                'name': 'Other Society Operations',
                'app_label': 'other_ops',
                'app_url': remaining[0].get('admin_url', '#'),
                'has_module_perms': True,
                'models': remaining,
            })

        return new_app_list

    site.get_app_list = custom_get_app_list

