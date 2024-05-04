from django.db import models
from apps.authentication.models import CustomUser
from django.utils import timezone

from datetime import datetime

class FamilyNode(models.Model):
    # id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(CustomUser, related_name='user_id', on_delete=models.CASCADE, default=None, null=True)
    id = models.JSONField(primary_key=True, unique=True)
    fid = models.JSONField(default=None, null=True)
    mid = models.JSONField(default=None, null=True)
    pids = models.JSONField(default=None, null=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, default=None, null=True)
    image = models.ImageField(upload_to='famTree/', null=True, blank=True)
    phone = models.IntegerField(default=0, null=True)
    email = models.EmailField(max_length=100, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField(default='2002-09-20', null=True)
    days_until_birthday = models.IntegerField(null=True, blank=True)
    special_event = models.CharField(max_length=100, default=None, null=True)
    other_comments = models.TextField(default=None, null=True)

    relationship = models.CharField(max_length=20, null=True) 
    total_members = models.IntegerField(default=0, null=True)
    total_male = models.IntegerField(default=0, null=True) 
    total_female = models.IntegerField(default=0, null=True)

    # Override the save method to calculate the relationship of the node
    def save(self, *args, **kwargs):
        if self.mid == self.id:
            self.relationship = "Mother"
        elif self.fid == self.id:
            self.relationship = "Father"
        elif self.pids and self.id in self.pids:
            self.relationship = "Parent"
        else:
            self.relationship = "Other"

        # Update family counts
        self.update_family_counts()

        super().save(*args, **kwargs)


    # Solving error Field 'phone' expected a number but got ''.
    def save(self, *args, **kwargs):
        if self.phone == '':
            self.phone = 0
        super(FamilyNode, self).save(*args, **kwargs)

    def __str__(self):
        return f"Node {self.id}: {self.name}"

class FamilyLink(models.Model):
    source_node = models.ForeignKey(FamilyNode, related_name='source_links', on_delete=models.CASCADE)
    target_node = models.ForeignKey(FamilyNode, related_name='target_links', on_delete=models.CASCADE)

    def __str__(self):
        return f"Link from {self.source_node} to {self.target_node}"