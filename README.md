django-app-skeleton
===================
This is merely my daily [`django`](https://djangoproject.com/ "Django Project site") application skeleton.

Both virtualenv and buildout approaches available
-------------------------------------------------
You can use both *buildout* and *virtualenv* approach with this skeleton.

For python virtual env use
```bash
$ ./virtualenv_setup.sh
```

For buildout configuration use
```bash
$ ./buildout_setup.sh
```

Packages included by default
----------------------------
* `django-grappelli` for better admin site look & feel
* `django-filebrowser` for admin site filebrowsing
* `south` for database migrations
* `django-rosetta` for admin i18n interface
* `django_jenkins` for jenkins CI server integration
* `djaml` for HAML template syntax

Layout versions
---------------
*twitter_bootstrap* branch uses the [Twitter Bootstrap](http://twitter.github.com/bootstrap/) theme.
[JQuery](jquery.com) and [HtmlShim](code.google.com/p/html5shim/) scripts are also used.
Master branch is currently basing on twitter_bootstrap branch. There are also bare skeleton branches.

Features included
-----------------
- authorization
    - frontend user basic authorization login via popup with redirection
    - frontend user logout with redirection
    - authorization implementation views, forms and templates
- user profiles
    - basic user profile model with django-filebrowser-compatible avatar field
    - profile view
    - edit profile view
    - change avatar view and form
- pluggable user list and user details views (disabled by default, see */accounts/urls.py*)
