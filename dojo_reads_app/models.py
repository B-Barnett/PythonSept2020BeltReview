from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        if len(postData['name']) < 2:
            errors['name'] = "Name is too short!"
        if len(postData['alias']) < 2:
            errors['alias'] = "Alias is too short!"
        if postData['password'] != postData['pass_confirm']:
            errors['password'] = "Password and password confirm do not match!"
        return errors
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if user:
            log_user = user[0]
            if not bcrypt.checkpw(postData['password'].encode(), log_user.password.encode()):
                errors['password'] = "Invalid login attempt"
        else:
            errors['password'] = "Invalid login attempt"
        return errors

class BookManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['title']) < 2:
            errors['title'] = "Title must be at least 2 characters!"
        if len(postData['author']) < 2:
            errors['author'] = "Author must be at least 2 characters!"
        return errors



class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=45)
    author = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name="reviews", on_delete=models.CASCADE)




#User model - Name, alias, email, password
#Book model - Title, Author
#Review model - Review content, rating, OtM with Users, OtM with Book