import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from axes.signals import user_locked_out
from axes.handlers.proxy import AxesProxyHandler

logger = logging.getLogger('forum_app')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    logger.info(f"SECURITY: Login Success | User: {user.username} | IP: {ip}")

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    username = user.username if user else "Unknown"
    logger.info(f"SECURITY: Logout | User: {username} | IP: {ip}")

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    ip = get_client_ip(request)
    username = credentials.get('username', 'unknown')
    if request and AxesProxyHandler.is_locked(request, credentials):
        return
    logger.warning(f"SECURITY: Login Failed | Attempted User: {username} | IP: {ip}")

@receiver(user_locked_out)
def log_user_lockout(request, username, ip_address, **kwargs):
    logger.error(f"SECURITY: Brute Force Lockout | User: {username} | IP: {ip_address}")