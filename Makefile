runserver:
	python3 main.py

freeze:
	pip3 freeze > requirements.txt

migrate:
	alembic upgrade head


