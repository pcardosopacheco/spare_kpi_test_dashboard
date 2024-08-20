clean:
	find . -name "*.pyc" -exec rm -rf {} \;

run:
	python manage.py runserver 0.0.0.0:8000

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

user:
	python manage.py createsuperuser

shell:
	python manage.py shell

exclude_migrations: clean
	rm **/migrations/[0-9]*.py

install:
	npm install
	bower install
	pip install -r requirements.txt
	make migrate

clean-install:
	make clean
	make install
