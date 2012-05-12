"""
User profile model
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from filebrowser.fields import FileBrowseField
from model_utils import Choices
from django.conf import settings

class UserProfile(models.Model):
    """
    Django user profile model
    """
    user = models.ForeignKey(to=User, null=False, blank=False, verbose_name=_('user'))
    first_name = models.CharField(max_length=100, verbose_name=_('first name'), null=False, blank=False, default=_('your first name'))
    last_name = models.CharField(max_length=100, verbose_name=_('last name'), null=False, blank=False, default=_('your last name'))
    middle_name = models.CharField(max_length=100, verbose_name=_('middle name'), null=True, blank=True)
    birth_date = models.DateField(verbose_name=_('birth date'), null=True, blank=True)
    phone = models.CharField(verbose_name=_('phone number'), null=False, blank=True, max_length=30)
    SEX = Choices(('male', _('male')), ('female', _('female')))
    sex = models.CharField(choices=SEX, default=SEX.male, max_length=10, verbose_name=_('sex'))
    avatar = FileBrowseField(verbose_name=_('avatar'), max_length=255)
    about = models.TextField(verbose_name=_('about'), null=True, blank=True)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    modified = models.DateTimeField(verbose_name=_('modified'), auto_now=True)

    def __unicode__(self):
        """
        return unicode representation
        """
        return self.user.__unicode__()

    @models.permalink
    def get_absolute_url(self):
        """
        return user profile url
        """
        return 'user', (), {'user_id': self.user.id}

    def update_avatar(self, new_avatar):
        """
        Update profile avatar with provided file
        """
        extension = new_avatar.content_type.split('/')[-1]
        if extension not in ['gif', 'jpg', 'jpeg', 'png']:
            raise ValueError(_('Wrong file extension / MIME type for avatar provided!'))
        with open("%s%d.%s" %(settings.AVATAR_STORAGE_PATH, self.user.id, extension) , 'wb') as destination:
            for chunk in new_avatar.chunks():
                destination.write(chunk)
        self.avatar = "%s%d.%s" % (settings.AVATAR_STORAGE_PATH_REL, self.user.id, extension)
        self.save()

#small handy hack
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
User.get_absolute_url = property(lambda u: u.profile.get_absolute_url())