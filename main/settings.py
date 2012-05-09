# -*- coding: utf-8 -*-
import os
from django.utils.translation import ugettext_lazy as _

# paths
PROJECT_ROOT_PATH = os.path.dirname(os.path.dirname(__file__)) + '/'
MEDIA_ROOT = PROJECT_ROOT_PATH + 'media/'
STATIC_ROOT = PROJECT_ROOT_PATH + 'static/'

# i18n
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True

# modeltranslation settings
LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
#    ('de', _('Deutch')),
#    ('es', _('Español')),
#    ('fr', _('Français')),
    )
LANGUAGE_CODE = 'ru'
MODEL_I18N_CONF = 'i18n_conf'
MODELTRANSLATION_DEFAULT_LANGUAGE = LANGUAGE_CODE
MODELTRANSLATION_TRANSLATION_REGISTRY = 'doppler.translation' #dunno what is it

SITE_ID = 1

ROOT_URLCONF = 'main.urls'

SECRET_KEY = '0q^^#b-w#ae@i%h$da%chx@3ldu52c5%6v)_fiaorkl+4#r%=1'

# static and media urls
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'grappelli/'

INSTALLED_APPS = (
	'south',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'rosetta',
    'djaml',
    'django_coverage',
    'django_jenkins',
    'modeltranslation',
    'main',
    'doppler',
    'doppler.shift.catalog',
    'doppler.shift.checkout',
)

# django_jenkins apps list
PROJECT_APPS = (
    'main',
    'doppler.shift.catalog',
    'doppler.shift.checkout',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
)

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
	'template_loaders.DjamlFilesystemLoader',
	'template_loaders.DjamlAppDirectoriesLoader',
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.request',
	'django.contrib.messages.context_processors.messages',
	'django.contrib.auth.context_processors.auth',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# registration and authorization settings
#ACCOUNT_ACTIVATION_DAYS = 2
#EMAIL_HOST = 'localhost'
#DEFAULT_FROM_EMAIL = 'gbezyuk@gmail.com'
#LOGIN_REDIRECT_URL = '/'
##LOGIN_URL = '/accounts/auth/login/'

# grappelli settings
GRAPPELLI_ADMIN_TITLE = "Admin site area"
#GRAPPELLI_INDEX_DASHBOARD = 'tulius.grappelli_dashboard.CustomIndexDashboard'

# filebrowser settings
FILEBROWSER_DIRECTORY = 'uploads/'
FILEBROWSER_VERSIONS_BASEDIR = 'uploads_versions/'
FILEBROWSER_VERSIONS = {
	'40x40': {
		'verbose_name':     u'40x40',
		'width':            40,
		'height':           40,
		'opts':             'crop',
	},
	'80x80': {
		'verbose_name':     u'80x80',
		'width':            80,
		'height':           80,
		'opts':             'crop',
	},
	'200x200': {
		'verbose_name':     u'200x200',
		'width':            200,
		'height':           200,
		'opts':             'crop',
	},
	'800x800': {
		'verbose_name':     u'800x800',
		'width':            800,
		'height':           800,
		'opts':             '',
	},
}
FILEBROWSER_ADMIN_VERSIONS = ['40x40', '80x80', '200x200', '800x800',]
FILEBROWSER_ADMIN_THUMBNAIL = '80x80'
FILEBROWSER_STRICT_PIL = True
FILEBROWSER_SEARCH_TRAVERSE = True
FILEBROWSER_DEFAULT_PERMISSIONS = 0755
FILEBROWSER_IMAGE_MAXBLOCK = 1024*1024*32
FILEBROWSER_URL_TINYMCE = '/static/grappelli/tinymce/jscripts/tiny_mce/'

# Doppler Shift engine configuration
DOPPLER_SHIFT_CATALOG_PRODUCT_MULTIPLE_PRICES = True
DOPPLER_SHIFT_CATALOG_PRODUCT_MULTIPLE_CATEGORIES = False