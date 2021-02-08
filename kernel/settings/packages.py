from .base import INSTALLED_APPS
from datetime import timedelta


# Third-Party Apps -->
INSTALLED_APPS.append('ckeditor')
INSTALLED_APPS.append('crispy_forms')
INSTALLED_APPS.append('hitcount')
INSTALLED_APPS.append('jalali_date')
INSTALLED_APPS.append('mptt')
INSTALLED_APPS.append('widget_tweaks')

# My Apps -->
INSTALLED_APPS.append('accounts.apps.AccountsConfig'),
INSTALLED_APPS.append('blog.apps.BlogConfig'),
INSTALLED_APPS.append('mysite.apps.MysiteConfig'),
INSTALLED_APPS.append('payment.apps.PaymentConfig'),
INSTALLED_APPS.append('rent.apps.RentConfig'),
INSTALLED_APPS.append('star_ratings.apps.StarRatingsAppConfig'),


AUTH_USER_MODEL = "accounts.User"

ALLOW_UNICODE_SLUGS = True

CKEDITOR_UPLOAD_PATH = "uploads/"

AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = ['accounts.backends.EmailBackend']


# Django Star Rating Config -->
STAR_RATINGS_RERATE = False
STAR_RATINGS_ANONYMOUS = False


# Jalali Date Config -->
# Defaults
JALALI_DATE_DEFAULTS = {
   'Strftime': {
        'date': '%y/%m/%d',
        'datetime': '%H:%M:%S _ %y/%m/%d',
    },
    'Static': {
        'js': [
            # Loading Datepicker -->
            'admin/js/django_jalali.min.js',
        ],
        'css': {
            'all': [
                'admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css',
            ]
        }
    },
}