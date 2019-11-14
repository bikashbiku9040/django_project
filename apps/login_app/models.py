"""import"""
from __future__ import unicode_literals
import datetime
import re
import bcrypt
from django.db import models


class UserManager(models.Manager):
    """User Manager Class"""

    def basic_validator(self, post_data):
        """Validator"""
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(post_data['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(post_data['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"
        email_regex = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # test whether a field matches the pattern
        if not email_regex.match(post_data['email']):
            errors['email'] = ("Invalid email address")
        user = User.objects.filter(email=post_data['email'])
        if user:
            errors['email'] = ("This email is taken")
        if post_data['birthday'] > datetime.datetime.now().strftime('%Y-%m-%d'):
            errors["birthday"] = "Birthday should not be in the future"
        birth_year = datetime.datetime.strptime(
            post_data['birthday'], '%Y-%m-%d').year
        age = datetime.datetime.now().year - birth_year
        if age < 13:
            errors["birthday"] = "You need to be at least 13 years old"
        if len(post_data['register_password']) < 8:
            errors["register_password"] = "Password should be at least 8 characters"
        if post_data['register_password'] != post_data['confirm_password']:
            errors["confirm_password"] = "Password does not match"
        return errors

    def create_user(self, post_data):
        """Create User and Securing Password using Bcrypt, pass back the user id"""
        password = post_data['register_password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        User.objects.create(first_name=post_data["first_name"], last_name=post_data["last_name"],
                            email=post_data["email"], birthday=post_data["birthday"],
                            password=pw_hash)
        return User.objects.last().id

    def get_user_id(self, post_data):
        """Check User email and passord to return User ID"""
        user = User.objects.filter(email=post_data["login_email"])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(post_data["login_password"].encode(), logged_user.password.encode()):
                return logged_user.id
        return

    def get_user_name(self, user_id):
        """Fetch User Name using id"""
        user = User.objects.filter(id=user_id)
        if user:
            logged_user = user[0]
            return f"{logged_user.first_name} {logged_user.last_name}"
        return


class User(models.Model):
    """User class"""
    # id
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
