from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext as _


class LoginRequired(LoginRequiredMixin):
    login_url = '/login/'
    login_required_message = _("You are not authorised! Please log in.")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.WARNING,
                                 self.login_required_message)
            return self.handle_no_permission()
        else:
            return super().dispatch(request, *args, **kwargs)
