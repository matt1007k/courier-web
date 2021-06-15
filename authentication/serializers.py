from rest_framework.serializers import ModelSerializer

from django.contrib.auth.models import AbstractUser, Group, Permission

class PermissionSerializer(ModelSerializer):
	class Meta:
		model = Permission
		fields = ['codename']

