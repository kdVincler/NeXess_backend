from django.db import models
from django.contrib.auth.models import User

# Create your models here.

perm_choices = [
    (0, "Level 0 - Guest"),
    (1, "Level 1 - Employee"),
    (2, "Level 2 - Specialist"),
    (3, "Level 3 - Deputy Manager"),
    (4, "Level 4 - Manager"),
    (5, "Level 5 - System Admin"),
    (6, "Level 6 - Director"),
]

class Door(models.Model):
    """Class to represent entry points, aka doors in the system"""
    descriptor = models.CharField(max_length=200, unique=True, null=False, default="Door description")
    perm_level = models.IntegerField(
        choices=perm_choices
    )

    def __str__(self):
        """Return the string representation of a door for readability in the admin site."""
        return f"Door {self.id} - {self.descriptor}; {self.get_perm_level_display()}"



class Permission(models.Model):
    """Class to house user entry permissions represented by an integer"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    perm_level = models.IntegerField(
        choices=perm_choices
    )

    def __str__(self):
        """Return the string representation of a permission level for readability in the admin site."""
        return f"User {self.user.username} has {self.get_perm_level_display()} level permission"


class Log(models.Model):
    """Class to show user entry logs"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    door = models.ForeignKey(Door, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    perm_granted = models.BooleanField(default=True)

    def __str__(self):
        """Return the string representation of a log entry for readability in the admin site."""
        return f"User {self.user.username} {'entered' if self.perm_granted else 'tried to enter'} door {self.door.id} at datetime {self.date_time}"
    
    def as_dict(self):
        """Return a dictionary representation of a log entry"""
        return {
            'uid': self.user.id,
            'door_id': self.door.id,
            'door_desc': self.door.descriptor,
            'accessed': self.date_time.strftime('%Y-%m-%d %H:%M'),
            'perm_granted': self.perm_granted
        }