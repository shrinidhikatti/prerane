# core/mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import DDPIProfile, BEOProfile, PrincipalProfile

class DDPIRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='DDPI').exists()
    
    def handle_no_permission(self):
        raise PermissionDenied("You must be a DDPI to access this page.")

class BEORequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='BEO').exists()
    
    def handle_no_permission(self):
        raise PermissionDenied("You must be a BEO to access this page.")

class PrincipalRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Principal').exists()
    
    def handle_no_permission(self):
        raise PermissionDenied("You must be a Principal to access this page.")

class RoleContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['is_ddpi'] = user.groups.filter(name='DDPI').exists()
        context['is_beo'] = user.groups.filter(name='BEO').exists()
        context['is_principal'] = user.groups.filter(name='Principal').exists()
        
        try:
            if context['is_ddpi']:
                context['user_profile'] = DDPIProfile.objects.get(user=user)
            elif context['is_beo']:
                context['user_profile'] = BEOProfile.objects.get(user=user)
            elif context['is_principal']:
                context['user_profile'] = PrincipalProfile.objects.get(user=user)
        except:
            context['user_profile'] = None
            
        return context