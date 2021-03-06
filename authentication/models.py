from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken

class UserManager(BaseUserManager):
	def create_user(self, username, email, password=None):
		if username is None:
			raise TypeError('Users should have username')
		if email is None:
			raise TypeError('Users should have an email')
			

		user = self.model(username=username, email=self.normalize_email(email))
		user.set_password(password)
		user.save()
		return user


	def create_superuser(self, username, email, password=None):
		if password is None:
			raise TypeError('Password should not be none')
		
		user = self.create_user(username, email, password)
		user.is_superuser = True
		user.is_staff = True
		user.save()
		return user		
		
class User(AbstractBaseUser, PermissionsMixin):
	username= models.CharField(max_length=255, unique=True, db_index=True)
	email= models.EmailField(max_length=255, unique=True, db_index=True)
	employeeID=models.CharField(max_length=20, null=True,blank=True)
	is_verified= models.BooleanField(default=True)
	is_active=models.BooleanField(default=True)
	is_staff=models.BooleanField(default=False)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)

	USERNAME_FIELD = 'username' #thisiscn
	REQUIRED_FIELDS=['email']

	objects = UserManager()

	def __str__(self):
		return self.username

	def tokens(self):
		token=RefreshToken.for_user(self)
		return {
			'refresh': str(token),
			'access': str(token.access_token)
		}