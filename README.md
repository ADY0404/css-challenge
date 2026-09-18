# Computer Science Society

A Django website for society activities, executive profiles, and member accounts.

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Optionally set `SECRET_KEY` in a `.env` file; a development-only fallback is included.
4. Run `python manage.py migrate` and then `python manage.py runserver`.

Run automated checks with `python manage.py test`.
