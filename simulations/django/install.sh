#!/bin/bash

source /tmp/netpipevenv/bin/activate
pip install --upgrade django django-admin

git clone https://github.com/jpadilla/django-project-template.git
cd django-project-template
django-admin.py startproject \
    --template=https://github.com/jpadilla/django-project-template/archive/master.zip \
    --name=Procfile \
    --extension=py,md,env \
    project_name >> /dev/null
cp ../example.env .env
cp ../manage.py .
cp ../settings.py ./project_name/settings.py
cp ../wsgi.py ./project_name/wsgi.py
cp ../urls.py ./project_name/urls.py
cp ../views.py ./project_name/views.py
cp -r ../templates ./project_name/
cp ../Procfile ./Procfile

pipenv install --dev

export DJANGO_SECRET_KEY=supersecret

echo "Running initial migration"
python manage.py migrate --noinput

echo ""
echo "Run ./start.sh to run Django"
