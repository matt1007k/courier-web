from rest_framework.serializers import ModelSerializer

from django.contrib.auth.models import AbstractUser, Group, Permission
from authentication.models import User

class UserSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = [
			'full_name',
			'email',
			'username',
			'avatar',
		]
		def full_name(self):
			return self.full_name()

class PermissionSerializer(ModelSerializer):
	class Meta:
		model = Permission
		fields = ['codename']
