from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import SuspiciousOperation
# Customized Mixin to ensure Multi-User Role Restrictions..
# Only Organizers can assign Agents.
# Agents can only see leads, etc

class LoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class OrganizerRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.is_organizer:
            
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)