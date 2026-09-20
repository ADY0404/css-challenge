# For security hardening - enforce unique email on auth_user

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_bio_profile_challenge_notifications_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="CREATE UNIQUE INDEX IF NOT EXISTS auth_user_email_unique ON auth_user(lower(email)) WHERE email <> '';",
            reverse_sql="DROP INDEX IF EXISTS auth_user_email_unique;",
        ),
    ]

