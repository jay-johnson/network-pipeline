#!/bin/bash

source /tmp/netpipevenv/bin/activate

pip install --upgrade django django-admin django-rest-swagger djangorestframework-jwt

git clone https://github.com/jpadilla/django-project-template.git
git clone https://github.com/szopu/django-rest-registration.git

cd django-rest-registration
pip install -e .
cd ..

cd django-project-template
django-admin.py startproject \
    --template=https://github.com/jpadilla/django-project-template/archive/master.zip \
    --name=Procfile \
    --extension=py,md,env \
    project_name >> /dev/null

pipenv install --dev

cp ../example.env .env
cp ../manage.py .
cp ../settings.py ./project_name/settings.py
cp ../wsgi.py ./project_name/wsgi.py
cp ../urls.py ./project_name/urls.py
cp ../api_user.py ./project_name/
cp ../serializer_user.py ./project_name/
cp ../create-super-user.sh create-super-user.sh
cp -r ../django-rest-registration/rest_registration/templates ./project_name/
cp -r ../templates/* ./project_name/
cp ../Procfile ./Procfile

export DJANGO_SECRET_KEY=supersecret

echo "Running makemigrations"
python manage.py makemigrations

echo "Running initial migration"
python manage.py migrate --noinput

./create-super-user.sh

echo ""
echo "Run ./start.sh to run Django"
