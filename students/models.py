from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


def getFilePath(instance, filename):
    return instance.path(filename)


class BaseModel(models.Model):
    date_added = models.BigIntegerField(
        editable=False, null=False, blank=True, db_column="date_added")
    last_modified = models.BigIntegerField(
        editable=False, null=False, blank=True, db_column="last_modified")
    deleted = models.BooleanField(
        editable=False, null=False, blank=True, db_column="deleted", default=False)

    class Meta:
        abstract = True


class Contact(BaseModel):
    contact_id = models.AutoField(
        editable=False, null=False, blank=True, db_column="contact_id", primary_key=True)
    contact_type = models.CharField(
        editable=True, null=False, blank=False, db_column="contact_type", max_length=100)
    contact_class = models.CharField(
        editable=True, null=False, blank=False, db_column="contact_class", max_length=100)
    contact = models.CharField(
        editable=True, null=False, blank=False, db_column="contact", max_length=1000)
    owner_type = models.CharField(
        editable=True, null=False, blank=False, db_column="owner_type", max_length=100)
    owner_id = models.CharField(
        editable=False, null=False, blank=True, db_column="owner_id", max_length=1000)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True,
                                 db_column="added_by", related_name="contactauthors")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, null=True, blank=True,
                                    db_column="modified_by", related_name="contactmodifiers")

    class Meta:
        db_table = 'contacts'


class User(AbstractUser):
    # user_id = models.AutoField(editable = False, null = False, blank = True, db_column = "user_id", primary_key = True)
    first_name = models.CharField(
        editable=True, null=False, blank=False, db_column="first_name", max_length=100)
    middle_name = models.CharField(
        editable=True, null=True, blank=True, db_column="middle_name", max_length=100)
    last_name = models.CharField(
        editable=True, null=False, blank=False, db_column="last_name", max_length=100)
    secondary_school = models.CharField(unique=True, editable=True,
                                        null=False, blank=False, db_column="secondary_school", max_length=100)
    date_of_birth = models.CharField(
        editable=True, null=True, blank=True, db_column="date_of_birth", max_length=100)
    gender = models.CharField(editable=True, null=False,
                              blank=False, db_column="gender", max_length=100)
    user_name = models.CharField(unique=True, editable=False,
                                 null=True, blank=True, db_column="user_name", max_length=100)
    secondary_school = models.CharField(editable=True,
                                        null=False, blank=False, db_column="secondary_school", max_length=100)
    county = models.CharField(editable=True,
                              null=False, blank=False, db_column="county", max_length=100)
    password = models.CharField(
        editable=False, null=True, blank=True, db_column="password", max_length=100)
    user_photo = models.FileField(upload_to=getFilePath, max_length=1000,
                                  editable=False, null=True, blank=True, db_column="user_photo")
    login_status = models.BooleanField(
        editable=False, null=True, blank=True, db_column="login_status", default=0)
    account_status = models.IntegerField(
        editable=False, null=True, blank=True, db_column="account_status", default=0)
    # USERNAME_FIELD = 'user_name'
    # EMAIL_FIELD = 'user_name'
    # REQUIRED_FIELDS = ['first_name', 'middle_name',
    #                    'last_name', 'date_of_birth', 'gender', 'username']

    class Meta:
        db_table = 'users'

    # def save(self, **kwargs):
    #     self.username = self.user_name
    #     self.email = self.user_name
    #     super(User, self).save(**kwargs)

    # @property
    # def dp_url(self):
    #     if self.user_photo and hasattr(self.user_photo, 'url'):
    #         return self.user_photo.url
    #     else:
    #         return f"/Assets/students/avatar.png"

    # def get_full_name(self):
    #     full_name = self.first_name + " " + self.last_name
    #     if(self.middle_name != None):
    #         full_name = self.first_name + " " + self.middle_name + " " + self.last_name
    #     return full_name

    # def get_short_name(self):
    #     return self.first_name
