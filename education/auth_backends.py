"""Prototype-only national-ID/mobile authentication; use OTP or password+MFA in production."""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import StudentProfile

class NationalIdMobileBackend(ModelBackend):
    def authenticate(self, request, national_id=None, mobile=None, **kwargs):
        if not national_id or not mobile: return None
        try:
            profile=StudentProfile.objects.select_related("user").get(national_id=national_id, mobile=mobile)
        except (StudentProfile.DoesNotExist, StudentProfile.MultipleObjectsReturned): return None
        return profile.user if profile.user.is_active else None
