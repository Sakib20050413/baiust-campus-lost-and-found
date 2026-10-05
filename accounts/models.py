from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

DEPARTMENT_CHOICES = [
    ('CSE', 'Computer Science & Engineering (CSE)'),
    ('EEE', 'Electrical & Electronic Engineering (EEE)'),
    ('CE', 'Civil Engineering (CE)'),
    ('BBA', 'Business Administration (BBA)'),
    ('ENG', 'English'),
    ('LAW', 'Law'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    student_id = models.CharField(max_length=30, unique=True, help_text="BAIUST Student or Staff ID")
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)
    phone_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.student_id})"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={'student_id': f"TEMP-{instance.id}", 'department': 'CSE'}
        )
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()

