from django.db import models
from django.contrib.auth.models import User

class Assignment(models.Model):
    subject = models.CharField(max_length=100, default="General")
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='assignments/', blank=True, null=True)
    gdrive_link = models.URLField(blank=True, null=True, help_text="Google Drive link for the assignment")
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_assignments')

    def __str__(self):
        return self.title

class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True, blank=True, related_name='submissions')
    file = models.FileField(upload_to='homeworks/', blank=True, null=True)
    submission_date = models.DateField(auto_now_add=True) # Changed to auto_now_add for simplicity
    gdrive_link = models.URLField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    checked_file = models.FileField(upload_to='checked_homeworks/', blank=True, null=True)
    checked_gdrive_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.date()}"

class Doubt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    file = models.FileField(upload_to='doubts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doubt by {self.user.username} at {self.created_at}"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notion_link = models.URLField(blank=True, null=True, help_text="Link to the student's Notion subject page")
    is_teacher = models.BooleanField(default=False, help_text="Designates whether this user is a teacher.")

    def __str__(self):
        return f"{self.user.username}'s Profile"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.studentprofile.save()
