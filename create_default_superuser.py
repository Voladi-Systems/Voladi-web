import os

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        'admin',
        f'admin@{os.getenv("VIRTUAL_HOST", "it@voladi.com")}',
        'adminadmin'
    )
