from django.db import models
from django.conf import settings

class Reminder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reminders')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    TYPE_CHOICES = [
        ('deadline', 'Deadline Alert'),
        ('test_due', 'Test Due Notification'),
        ('pending', 'Pending Lesson'),
        ('general', 'General'),
    ]
    reminder_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='general')

    def __str__(self):
        return f"{self.user.username} - {self.message[:20]}"
