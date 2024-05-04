from django.db import models
from apps.authentication.models import CustomUser
from django.utils import timezone
from datetime import datetime, date

from datetime import datetime

class PersonalInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='personal_info')
    bio = models.TextField(max_length=500, blank=True)
    age = models.IntegerField(null=True, blank=True)
    position = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    days_until_birthday = models.IntegerField(null=True, blank=True)
    upcoming_age = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    instagram = models.CharField(max_length=50, blank=True)
    facebook = models.CharField(max_length=50, blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    linkedin = models.CharField(max_length=50, blank=True)
    background_image = models.ImageField(upload_to='background_images/', null=True, blank=True)

 
    # Override the save method to calculate the days until the user's birthday
    def save(self, *args, **kwargs):
        if self.birth_date:
            today = datetime.now()
            
            # Ensure self.birth_date is a string
            if isinstance(self.birth_date, date):
                birth_date_str = self.birth_date.strftime('%Y-%m-%d')
            else:
                birth_date_str = self.birth_date
            
            birth_datetime = datetime.strptime(birth_date_str, '%Y-%m-%d')
            birthday = birth_datetime.replace(year=today.year)
            
            if birthday < today:
                birthday = birthday.replace(year=today.year + 1)
            
            self.days_until_birthday = (birthday - today).days
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery_images/')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='gallery_images')
    
    def __str__(self):
        return self.user.email

class Timeline(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='timeline')
    description = models.TextField(max_length=500)
    event_title = models.CharField(max_length=50)
    event_description = models.TextField(max_length=500)
    date = models.DateField()
    time = models.TimeField()


    def __str__(self):
        return self.event_title


class Question(models.Model):
    question_text = models.TextField()
    option_one = models.CharField(max_length=200)
    option_two = models.CharField(max_length=200)
    option_three = models.CharField(max_length=200)
    option_four = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

class QuizResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to the user
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date_taken.strftime('%Y-%m-%d %H:%M')}"