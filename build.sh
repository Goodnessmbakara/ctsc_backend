#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate


EMAIL="admin@example.com"
PASSWORD="supersecret"
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
if get_user_model().objects.filter(email="$EMAIL"):
    print("User $EMAIL already exists")
else:
    get_user_model().objects.create_superuser('$EMAIL', '$PASSWORD')
    print('Superuser "$EMAIL" created successfully.')
EOF
