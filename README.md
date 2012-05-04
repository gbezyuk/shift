django-app-skeleton
===================
This is merely my daily [`django`](https://djangoproject.com/ "Django Project site") application skeleton.

Both virtualenv and buildout approaches available
-------------------------------------------------
You can use both *buildout* and *virtualenv* approach with this skeleton.
    $ # for python virtual env use
    $ ./virtualenv_setup.sh
    $
    $ # for builout configuration use
    $ ./builout_setup.sh

Packages included by default
----------------------------
* `django-grappelli` for better admin site look & feel
* `django-filebrowser` for admin site filebrowsing
* `south` for database migrations
* `django-rosetta` for admin i18n interface
* `django_jenkins` for jenkins CI server integration
* `djaml` for HAML template syntax

