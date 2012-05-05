import os

PROJECT_ROOT_PATH = os.path.dirname(os.path.dirname(__file__)) + '/'
MEDIA_ROOT = PROJECT_ROOT_PATH + 'media/'
STATIC_ROOT = PROJECT_ROOT_PATH + 'static/'

ROOT_URLCONF = 'main.urls'

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-ru'
USE_I18N = True
USE_L10N = True
SITE_ID = 1

SECRET_KEY = '0q^^#b-w#ae@i%h$da%chx@3ldu52c5%6v)_fiaorkl+4#r%=1'

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
    'main',
    'doppler.shift.catalog',
)

PROJECT_APPS = (
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

ACCOUNT_ACTIVATION_DAYS = 2
EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'gbezyuk@gmail.com'
LOGIN_REDIRECT_URL = '/'
#LOGIN_URL = '/accounts/auth/login/'


GRAPPELLI_ADMIN_TITLE = "Admin site area"
#GRAPPELLI_INDEX_DASHBOARD = 'tulius.grappelli_dashboard.CustomIndexDashboard'

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

FILEBROWSER_ADMIN_VERSIONS = [
	'40x40',
	'80x80',
	'200x200',
	'800x800',
]

FILEBROWSER_ADMIN_THUMBNAIL = '80x80'
FILEBROWSER_STRICT_PIL = True
FILEBROWSER_SEARCH_TRAVERSE = True
FILEBROWSER_DEFAULT_PERMISSIONS = 0755
FILEBROWSER_IMAGE_MAXBLOCK = 1024*1024*32
FILEBROWSER_URL_TINYMCE = '/static/grappelli/tinymce/jscripts/tiny_mce/'
