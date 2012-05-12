from django.views.generic.simple import direct_to_template, redirect_to
from django.contrib import messages
from .forms import ProfileForm, ChangeAvatarForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

@login_required
def profile(request, template_name='accounts/profile.haml'):
    profile_form = ProfileForm(data=request.POST or None, instance=request.user.profile)
    return direct_to_template(request, template_name, locals())

@login_required
def edit_profile(request, template_name='accounts/edit_profile.haml'):
    form = ProfileForm(data=request.POST or None, instance=request.user.profile)
    if form.is_valid():
        form.save()
        messages.success(request, form.update_success_message)
        return redirect_to(request, reverse('profile'), permanent=False)
    elif request.POST:
        messages.error(request, form.validation_failed_message)
    return direct_to_template(request, template_name, locals())

@login_required
def change_avatar(request, template_name='accounts/change_avatar.haml'):
    form = ChangeAvatarForm(data=request.POST or None,
        instance=request.user.profile,
        files=request.FILES)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, form.update_success_message)
        return redirect_to(request, reverse('profile'), permanent=False)
    elif request.POST:
        messages.error(request, form.validation_failed_message)
    return direct_to_template(request, template_name, locals())

#TODO: superuser only?
def users(request, template_name='accounts/users.haml'):
    users = User.objects.all()
    return direct_to_template(request, template_name, locals())
