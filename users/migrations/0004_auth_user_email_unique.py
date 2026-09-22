# For security hardening - enforce unique email on auth_user across all supported databases

from django.db import migrations


def create_unique_email_index(apps, schema_editor):
    connection = schema_editor.connection
    vendor = connection.vendor
    with connection.cursor() as cursor:
        if vendor == 'postgresql':
            cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS auth_user_email_unique ON auth_user(lower(email)) WHERE email <> '';")
        elif vendor == 'sqlite':
            cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS auth_user_email_unique ON auth_user(lower(email)) WHERE email <> '';")
        elif vendor == 'mysql':
            # In MariaDB / MySQL
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.statistics 
                WHERE table_schema = DATABASE() AND table_name = 'auth_user' AND index_name = 'auth_user_email_unique'
            """)
            row = cursor.fetchone()
            if not row or row[0] == 0:
                cursor.execute("CREATE UNIQUE INDEX auth_user_email_unique ON auth_user(email);")


def drop_unique_email_index(apps, schema_editor):
    connection = schema_editor.connection
    vendor = connection.vendor
    with connection.cursor() as cursor:
        if vendor == 'mysql':
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.statistics 
                WHERE table_schema = DATABASE() AND table_name = 'auth_user' AND index_name = 'auth_user_email_unique'
            """)
            row = cursor.fetchone()
            if row and row[0] > 0:
                cursor.execute("DROP INDEX auth_user_email_unique ON auth_user;")
        else:
            cursor.execute("DROP INDEX IF EXISTS auth_user_email_unique;")


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_bio_profile_challenge_notifications_and_more'),
    ]

    operations = [
        migrations.RunPython(create_unique_email_index, drop_unique_email_index),
    ]
