from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from PIL import Image
from django.core.files.storage import default_storage as storage



class HRTeamUser(models.Model):
  id = models.AutoField(db_column='ID', primary_key=True)
  firstname = models.CharField(db_column='FirstName', max_length=15)
  lastname = models.CharField(db_column='LastName', max_length=15)
  userid = models.CharField(db_column='UserID', max_length=8, unique=True)
  password = models.CharField(db_column='Password', max_length=9)
  ssn = models.CharField(db_column='SSN', max_length=11)
  dob = models.DateField(db_column='DOB')
  department = models.CharField(db_column='Department', max_length=20)
  jobtitle = models.CharField(db_column='JobTitle', max_length=80)
  accesslevel = models.CharField(db_column='AccessLevel', max_length=20)
  dateofhire = models.DateField(db_column='DateOfHire')
  email = models.CharField(db_column='Email', max_length=40)
  address = models.CharField(db_column='Address', max_length=50)
  city = models.CharField(db_column='City', max_length=15)
  state = models.CharField(db_column='State', max_length=2)
  zipcode = models.IntegerField(db_column='ZipCode')
  phone = models.CharField(db_column='Phone', max_length=14)
  cell = models.CharField(db_column='Cell', max_length=14)
  is_active = models.BooleanField(db_column='Is_Active', default=True)

  def __str__(self):
    return self.userid

  def get_short_job_title(self):
    if self.accesslevel == "Associate":
      job = str(self.jobtitle)
      job_words = job.split(' - ')
      self.associate_title = job_words[0]
      return self.associate_title
    else:
      return self.jobtitle

  def get_hr_group(self):
    if self.accesslevel == "Associate":
      job = str(self.jobtitle)
      job_titles = job.split(' - ')
      self.hr_group = job_titles[1]
      return self.hr_group
    else:
      return "HR Management"
	    
  class Meta:
	  managed = False
	  app_label = 'accounts'
	  db_table = 'HR_Dept_Team'



class CustomUser(AbstractUser):
  userid = models.CharField(db_column='User_ID', max_length=8, unique=True)
  password = models.CharField(db_column='Password', max_length=140) 
  email = models.CharField(db_column='Email', max_length=80)
  accesslevel = models.CharField(db_column='Access_Level', max_length=30)
  hrgroup = models.CharField(db_column='HR_Group', max_length=80)
  is_superuser = models.BooleanField(db_column='Is_SuperUser', default=False)
  is_staff = models.BooleanField(db_column='Is_Staff', default=False)
  is_active = models.BooleanField(db_column='Is_Active', default=True)

  def __str__(self):
    return self.userid

  def hr_group(self):
    return self.hrgroup

  def access_level(self):
    return self.accesslevel

  class Meta:
    managed = True
    app_label = 'accounts'
    verbose_name = 'HR Team User'
    verbose_name_plural = 'HR Team Users'



class Profile(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  image = models.ImageField(default='default.png', upload_to='profile_pics')

  def __str__(self):
    return f'{self.user.username} Profile'

  def save(self, *args, **kwargs):
    super(Profile, self).save(*args, **kwargs)
    img = Image.open(storage.open(self.image.name))    
    if img.height > 100 or img.width > 100:
        output_size = (100, 100)
        img.thumbnail(output_size)
        img.save(storage.open(self.image.name))

  class Meta:
    app_label = 'accounts'
    verbose_name = 'User Profile'
    verbose_name_plural = 'User Profiles'