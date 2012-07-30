from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from ..checkout.signals import order_created, order_state_changed
#from feedback.signals import feedback_message_created
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.models import Site
#from django.core.mail import EmailMultiAlternatives

#@receiver(feedback_message_created)
#def feedback_message_created_notification (sender, feedback_message, **kwargs):
#
#	ctx_dict = {
#		'feedback_message': feedback_message,
#		'site': Site.objects.get(id=settings.SITE_ID)
#	}
#
#	subject = render_to_string('notifications/superuser/feedback_message_created_subject.txt', ctx_dict)
#	subject = ''.join(subject.splitlines())
#	message = render_to_string('notifications/superuser/feedback_message_created.txt', ctx_dict)
#	superusers = User.objects.filter(is_active=True, is_superuser=True)
#	for superuser in superusers:
#		superuser.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
#
#	subject = render_to_string('notifications/user/feedback_message_created_subject.txt', ctx_dict)
#	subject = ''.join(subject.splitlines())
#	message = render_to_string('notifications/user/feedback_message_created.txt', ctx_dict)
#	feedback_message.author.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
#
#	if feedback_message.author.manager:
#		subject = render_to_string('notifications/manager/feedback_message_created_subject.txt', ctx_dict)
#		subject = ''.join(subject.splitlines())
#		message = render_to_string('notifications/manager/feedback_message_created.txt', ctx_dict)
#		feedback_message.author.manager.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

@receiver(order_created)
def order_created_notification (sender, order, **kwargs):
    ctx_dict = {
        'order': order,
        'site': Site.objects.get(id=settings.SITE_ID)
    }

    subject = render_to_string('notifications/superuser/new_order_subject.txt', ctx_dict)
    subject = ''.join(subject.splitlines())
    message = render_to_string('notifications/superuser/new_order.txt', ctx_dict)

    superusers = User.objects.filter(is_active=True, is_superuser=True)
    for superuser in superusers:
        superuser.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    if order.user:
        subject = render_to_string('notifications/user/new_order_subject.txt', ctx_dict)
        subject = ''.join(subject.splitlines())
        message = render_to_string('notifications/user/new_order.txt', ctx_dict)
        order.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

#		if order.user.manager:
#			subject = render_to_string('notifications/manager/new_order_subject.txt', ctx_dict)
#			subject = ''.join(subject.splitlines())
#			message = render_to_string('notifications/manager/new_order.txt', ctx_dict)
#			order.user.manager.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)


@receiver(order_state_changed)
def order_state_changed_notification (sender, order, **kwargs):

    ctx_dict = {
        'order': order,
        'site': Site.objects.get(id=settings.SITE_ID)
    }

    subject = render_to_string('notifications/superuser/order_state_changed_subject.txt', ctx_dict)
    subject = ''.join(subject.splitlines())
    message = render_to_string('notifications/superuser/order_state_changed.txt', ctx_dict)

    superusers = User.objects.filter(is_active=True, is_superuser=True)
    for superuser in superusers:
        superuser.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    if order.user:
        subject = render_to_string('notifications/user/order_state_changed_subject.txt', ctx_dict)
        subject = ''.join(subject.splitlines())
        message = render_to_string('notifications/user/order_state_changed.txt', ctx_dict)
        order.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

#        if order.user.manager:
#            subject = render_to_string('notifications/manager/order_state_changed_subject.txt', ctx_dict)
#            subject = ''.join(subject.splitlines())
#            message = render_to_string('notifications/manager/order_state_changed.txt', ctx_dict)
#            order.user.manager.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

#notify_new_user_registration_flag = False
#
#@receiver(pre_save)
#def user_pre_save_handler (sender, instance, **kwargs):
#	from django.contrib.auth.models import User
#	if sender == User:
#		if not getattr(instance, 'id', False):
#			global notify_new_user_registration_flag
#			notify_new_user_registration_flag = True
#		else:
#			old_user_state = User.objects.get(id=instance.id)
#			if not old_user_state.is_active and instance.is_active:
#				notify_user_activation(instance)
#			if old_user_state.is_active and not instance.is_active:
#				notify_user_deactivation(instance)
#			if old_user_state.manager != instance.manager:
#				notify_user_manager_change(instance, old_user_state)
#			if old_user_state.is_staff and not instance.is_staff:
#				notify_user_staff_rights_lost(instance)
#			if not old_user_state.is_staff and instance.is_staff:
#				notify_user_staff_rights_aquired(instance)
#			if old_user_state.is_superuser and not instance.is_superuser:
#				notify_user_superuser_rights_lost(instance)
#			if not old_user_state.is_superuser and instance.is_superuser:
#				notify_user_superuser_rights_aquired(instance)
#
#@receiver(post_save)
#def user_post_save_handler (sender, instance, **kwargs):
#	from django.contrib.auth.models import User
#	if sender == User:
#		global notify_new_user_registration_flag
#		if notify_new_user_registration_flag:
#			notify_new_user_registration(instance)
#			notify_new_user_registration_flag = False
#
#def _get_context_dict(user):
#	try:
#		site = Site.objects.get(id=settings.SITE_ID)
#	except:
#		site = None
#	return {
#		'user': user,
#		'site': site
#	}
#
#def send_user_notification_message(recipients, template_name, context_dictionary):
#	subject = render_to_string(template_name + '_subject.txt', context_dictionary)
#	subject = ''.join(subject.splitlines())
#	message = render_to_string(template_name + '.txt', context_dictionary)
#	if getattr(recipients, '__iter__', False):
#		for recipient in recipients:
#			recipient.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
#	else:
#		# the only recipeint provided
#		recipients.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
#
#def get_superusers():
#	return User.objects.filter(is_active=True, is_superuser=True)
#
#def notify_new_user_registration(user):
#	context_dictionary = _get_context_dict(user)
#	superusers = get_superusers()
#	send_user_notification_message(
#		superusers,
#		'notifications/superuser/user/registred',
#		context_dictionary,
#	)
#	if user.manager:
#		send_user_notification_message(
#			user.manager,
#			'notifications/manager/user/registred',
#			context_dictionary,
#		)
#	send_user_notification_message(
#		user,
#		'notifications/user/registred',
#		context_dictionary,
#	)
#
#def notify_user_activation(user):
#	context_dictionary = _get_context_dict(user)
#	superusers = get_superusers()
#	send_user_notification_message(
#		superusers,
#		'notifications/superuser/user/activated',
#		context_dictionary,
#	)
#	if user.manager:
#		send_user_notification_message(
#			user.manager,
#			'notifications/manager/user/activated',
#			context_dictionary,
#		)
#	send_user_notification_message(
#		user,
#		'notifications/user/activated',
#		context_dictionary,
#	)
#
#def notify_user_deactivation(user):
#	context_dictionary = _get_context_dict(user)
#	superusers = get_superusers()
#	send_user_notification_message(
#		superusers,
#		'notifications/superuser/user/deactivated',
#		context_dictionary,
#	)
#	if user.manager:
#		send_user_notification_message(
#			user.manager,
#			'notifications/manager/user/deactivated',
#			context_dictionary,
#		)
#	send_user_notification_message(
#		user,
#		'notifications/user/deactivated',
#		context_dictionary,
#	)
#
#def notify_user_manager_change(user, old_user):
#	from django.contrib.auth.models import User
#	context_dictionary = _get_context_dict(user)
#	superusers = get_superusers()
#	send_user_notification_message(
#		superusers,
#		'notifications/superuser/user/manager_changed',
#		context_dictionary,
#	)
#
#	if old_user.manager:
#		send_user_notification_message(
#			old_user.manager,
#			'notifications/manager/user/client_lost',
#			context_dictionary,
#		)
#
#	if user.manager:
#		send_user_notification_message(
#			user.manager,
#			'notifications/manager/user/client_aquired',
#			context_dictionary,
#		)
#
#	send_user_notification_message(
#		user,
#		'notifications/user/manager_changed',
#		context_dictionary,
#	)
#
#def notify_user_staff_rights_aquired(user):
#	context_dictionary = _get_context_dict(user)
#	superusers = get_superusers()
#	send_user_notification_message(
#		superusers,
#		'notifications/superuser/user/staff_rights_aquired',
#		context_dictionary,
#	)
#	send_user_notification_message(
#		user,
#		'notifications/user/staff_rights_aquired',
#		context_dictionary,
#	)
#
#def notify_user_staff_rights_lost(user):
#	context_dictionary = _get_context_dict(user)
#	superusers = get_superusers()
#	send_user_notification_message(
#		superusers,
#		'notifications/superuser/user/staff_rights_lost',
#		context_dictionary,
#	)
#	send_user_notification_message(
#		user,
#		'notifications/user/staff_rights_lost',
#		context_dictionary,
#	)
#
#def notify_user_superuser_rights_aquired(user):
#	context_dictionary = _get_context_dict(user)
#	superusers = get_superusers()
#	send_user_notification_message(
#		superusers,
#		'notifications/superuser/user/superuser_rights_aquired',
#		context_dictionary,
#	)
#	send_user_notification_message(
#		user,
#		'notifications/user/superuser_rights_aquired',
#		context_dictionary,
#	)
#
#def notify_user_superuser_rights_lost(user):
#	context_dictionary = _get_context_dict(user)
#	superusers = get_superusers()
#	send_user_notification_message(
#		superusers,
#		'notifications/superuser/user/superuser_rights_lost',
#		context_dictionary,
#	)
#	send_user_notification_message(
#		user,
#		'notifications/user/superuser_rights_lost',
#		context_dictionary,
#	)