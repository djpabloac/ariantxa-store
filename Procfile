release: python ecommerce/manage.py migrate
web: cd ecommerce && gunicorn ecommerce.wsgi --log-file - && python manage.py migrate && python manage.py runserver