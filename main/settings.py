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
    'rollyourown.seo',
    'utils',
    'accounts',
    'compressor',
    'mptt',
    'pagetree',
    'main',
    'doppler',
    'doppler.shift.catalog',
    'doppler.shift.checkout',
    'doppler.shift.notifications',
    'social_auth',
    'registration',
    'flatblocks',
    'robokassa',
)

# django_jenkins apps list
PROJECT_APPS = (
    'accounts',
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
    'session_cart.middleware.SimpleCartMiddleware',
    'doppler.shift.catalog.middleware.ProductFallbackMiddleware',
    'doppler.shift.catalog.middleware.CategoryFallbackMiddleware',
    'pagetree.middleware.PageFallbackMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
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
    'main.context_processors.login_url',
    'main.context_processors.default_avatar_url',
    'doppler.shift.catalog.context_processors.categories',
    'session_cart.context_processors.carts',
    'pagetree.context_processors.root_pages',
    'social_auth.context_processors.social_auth_by_type_backends',
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

ACCOUNT_ACTIVATION_DAYS = 7
EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'gbezyuk@gmail.com'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/auth/login/'

# grappelli settings
GRAPPELLI_ADMIN_TITLE = _("WesternUnit.Ru Shop Administration")
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
    '300x300': {
        'verbose_name':     u'300x300',
        'width':            300,
        'height':           300,
        'opts':             '',
        },
    '800x800': {
        'verbose_name':     u'800x800',
        'width':            800,
        'height':           800,
        'opts':             '',
    },
    '420x260': {
        'verbose_name':     u'420x260',
        'width':            420,
        'height':           260,
        'opts':             '',
        },
    '300x186': {
        'verbose_name':     u'300x186',
        'width':            300,
        'height':           186,
        'opts':             '',
        },
    '150x93': {
        'verbose_name':     u'150x93',
        'width':            150,
        'height':           93,
        'opts':             '',
        },
}
FILEBROWSER_ADMIN_VERSIONS = ['40x40', '80x80', '150x93', '300x186', '420x260', '200x200', '800x800',]
FILEBROWSER_ADMIN_THUMBNAIL = '150x93'
FILEBROWSER_STRICT_PIL = True
FILEBROWSER_SEARCH_TRAVERSE = True
FILEBROWSER_DEFAULT_PERMISSIONS = 0755
FILEBROWSER_IMAGE_MAXBLOCK = 1024*1024*32
FILEBROWSER_URL_TINYMCE = '/static/grappelli/tinymce/jscripts/tiny_mce/'

DEFAULT_AVATAR_URL = MEDIA_URL + 'img/default-avatar.gif'
AVATAR_STORAGE_PATH_REL = FILEBROWSER_DIRECTORY + 'avatars/'
AVATAR_STORAGE_PATH = MEDIA_ROOT + AVATAR_STORAGE_PATH_REL

DOPPLER_SHIFT_CATALOG_PRODUCT_MULTIPLE_PRICES = True
DOPPLER_SHIFT_CATALOG_PRODUCT_MULTIPLE_CATEGORIES = False

COMPRESS_URL = '/'
COMPRESS_ROOT = PROJECT_ROOT_PATH
COMPRESS_ENABLED = True
COMPRESS_OUTPUT_DIR = 'media/CACHE'
COMPRESS_PRECOMPILERS = (
#    ('text/coffeescript', 'coffee --compile --stdio'),
#    ('text/less', 'lessc {infile} {outfile}'),
    ('text/x-sass', 'sass {infile} {outfile}'),
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
    )

CART_MODEL = 'doppler.shift.catalog.models.Price'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.contrib.vkontakte.VKontakteOAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UUID_LENGTH = 16
SOCIAL_AUTH_EXTRA_DATA = True

VKONTAKTE_APP_ID = 3035044   # see http://vk.com/app3035044
VKONTAKTE_APP_SECRET = 'lh0BfIdOw2AYnKBB8KBb'
#Twitter is buggy, so disabled yet
#TWITTER_CONSUMER_KEY = '7Qk1hrbqcYPuzJng0IDMw' # contact gbezyuk@gmail.com if neccessary
#TWITTER_CONSUMER_SECRET = 'c4NEx3qunxwuwIYsWDzZZmSByX7buVu3isF4IQjh8'
FACEBOOK_APP_ID = '308278985935273' # see https://developers.facebook.com/apps/308278985935273/
FACEBOOK_API_SECRET = 'ba31d528427aada31eb841bd764815d3'
GOOGLE_CONSUMER_KEY = 'westernunit.ru' # contact gbezyuk@gmail.com if neccessary
GOOGLE_CONSUMER_SECRET = 'vuhwjp1IWmdwUYWQWQgcBeDV'
