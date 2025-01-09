from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import AccessMixin


class RedirectAuthenticatedUserMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('job_home'))
        return super().dispatch(request, *args, **kwargs)
