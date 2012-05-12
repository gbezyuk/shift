from .models import UserProfile
from django import forms
from django.utils.translation import ugettext_lazy as _

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'avatar',]

    html_class = 'profile_form'
    html_id = 'profile_form'

    update_success_message = _('Your profile is successfully updated')
    validation_failed_message = _('There were some errors during form validation')

class ChangeAvatarForm(forms.Form):
    avatar = forms.FileField(required=True, help_text=_('upload new avatar file'), label=_('avatar'))

    html_class = 'change_avatar_form'
    html_id = 'change_avatar_form'

    update_success_message = _('Your profile avatar is successfully updated')
    validation_failed_message = _('There were some errors during form validation')

    def __init__(self, *args, **kwargs):
        if not 'instance' in kwargs:
            raise AttributeError(_('ChangeAvatarForm haven`t got the profile instance'))
        self.instance = kwargs.pop('instance')
        super(ChangeAvatarForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        uploaded_avatar = self.files['avatar']
        user_profile = self.instance
        user_profile.update_avatar(uploaded_avatar)
        return user_profile