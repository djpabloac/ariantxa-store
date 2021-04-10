release: python ecommerce/manage.py migrate
web: cd ecommerce
web: gunicorn ecommerce.wsgi --log-file -