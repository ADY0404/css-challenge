rs: 
	@python3 manage.py runserver 3000

mm:
	@python3 manage.py makemigrations

m:
	@python3 manage.py migrate

su:
	@python3 manage.py createsuperuser
