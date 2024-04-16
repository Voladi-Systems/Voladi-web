from os import environ

from django.utils.translation import gettext_lazy as _
from dotenv import dotenv_values

from povulo.settings import *
from povulo.settings import (
    DEFAULT_INSTALLED_APPS,
    DEFAULT_LANG,
    DEFAULT_LOGGING,
)


env = {
    **dotenv_values('.env.local'),  # reading .env file for local dev only
    **environ,  # override loaded values with environment variables
}

INSTALLED_APPS = DEFAULT_INSTALLED_APPS

TEMPLATES[0]['OPTIONS']['context_processors'].append('web.context.general')


LOGGING = DEFAULT_LOGGING

# Add languages as needed
LANGUAGES = (
    DEFAULT_LANG,
    ('bg', 'Bulgarian'),
    ('zh', 'Chinese'),
    ('cs', 'Czech'),
    ('da', 'Danish'),
    ('nl', 'Dutch'),
    ('et', 'Estonian'),
    ('fi', 'Finnish'),
    ('fr', 'French'),
    ('de', 'German'),
    ('el', 'Greek'),
    ('hu', 'Hungarian'),
    ('id', 'Indonesian'),
    ('it', 'Italian'),
    ('ja', 'Japanese'),
    ('ko', 'Korean'),
    ('lv', 'Latvian'),
    ('lt', 'Lithuanian'),
    ('nb', 'Norwegian (bokmål)'),
    ('pl', 'Polish'),
    ('pt', 'Portuguese'),
    ('ro', 'Romanian'),
    ('ru', 'Russian'),
    ('sk', 'Slovak'),
    ('sl', 'Slovenian'),
    ('es', 'Spanish'),
    ('sv', 'Swedish'),
    ('tr', 'Turkish'),
    ('uk', 'Ukrainian'),
)

LOCALE_PATHS = [
    BASE_DIR / 'locales',
]

WAGTAIL_CONTENT_LANGUAGES = LANGUAGES

WAGTAIL_SITE_NAME = 'voladi'
