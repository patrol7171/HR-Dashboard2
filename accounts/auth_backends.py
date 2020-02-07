from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from .models import HRTeamUser
import random
from random import randint


class AuthBackend(object):
	def authenticate(self, request, username=None, password=None):
		account = get_user_model()	
		if username is None or password is None:
			return None	
		else:
			try:
				hrUser = account.objects.get(userid=username)
				if hrUser.check_password(password):
					return hrUser	
			except account.DoesNotExist:
				try:
					userInfo = HRTeamUser.objects.get(userid=username)
					if password == userInfo.password:
						newUser = account(username=username)
						newUser.password = make_password(password)
						newUser.userid = userInfo.userid
						newUser.first_name = userInfo.firstname
						newUser.last_name = userInfo.lastname
						newUser.email = userInfo.email
						newUser.accesslevel = userInfo.accesslevel
						newUser.hrgroup = userInfo.get_hr_group()
						newUser.is_staff = False
						newUser.is_superuser = False				
						newUser.save()
						newUser_group, created = Group.objects.get_or_create(name=newUser.accesslevel)
						newUser.groups.add(newUser_group) 
						return newUser
					else:
						return None
				except HRTeamUser.DoesNotExist:
					login_valid = (settings.ADMIN_LOGIN == username)
					pwd_valid = (settings.ADMIN_PASSWORD == password)
					if login_valid and pwd_valid:
						newID = ''.join(["%s" % randint(0, 9) for num in range(0, 3)])					
						admin = account(username = username+newID)
						admin.userid = username + newID
						admin.password = make_password(password)
						admin.first_name = admin.userid.capitalize()
						admin.email = "hradmin@dentalmagic.com"
						admin.accesslevel = "Admin"
						admin.hrgroup = "HR Management"
						admin.is_staff = True
						admin.is_superuser = False
						admin.has_perm = True
						admin.save()						
						admin_group,created = Group.objects.get_or_create(name='Admin')
						admin.groups.add(admin_group) 												
						return admin
					else:
						print("Unauthorized to access this site.")
						return None


	def get_user(self, pk):
		try:
			userAcct = get_user_model()
			return userAcct.objects.get(pk=pk)
		except userAcct.DoesNotExist:
			return None
