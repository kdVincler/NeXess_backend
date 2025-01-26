from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Door(models.Model):
    """Class to represent entry points, aka doors in the system"""
    descriptor = models.CharField(max_length=200, null=False, default="Door description")
    perm_level = models.IntegerField(
        choices=[
            (0, "Permission level 0"),
            (1, "Permission level 1"),
            (2, "Permission level 2"),
            (3, "Permission level 3"),
            (4, "Permission level 4"),
            (5, "Permission level 5"),
        ]
    )

    def __str__(self):
        """Return the string representation of a door for readability in the admin site."""
        return f"Door {self.id}, {self.descriptor} - Permission level: {self.perm_level}"



class Permission(models.Model):
    """Class to house user entry permissions represented by an integer"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    perm_level = models.IntegerField(
        choices=[
            (0, "Permission level 0"),
            (1, "Permission level 1"),
            (2, "Permission level 2"),
            (3, "Permission level 3"),
            (4, "Permission level 4"),
            (5, "Permission level 5"),
        ]
    )

    def __str__(self):
        """Return the string representation of a permission level for readability in the admin site."""
        return f"User {self.user.username} has permission level {self.perm_level}"


class Log(models.Model):
    """Class to show user entry logs"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    door = models.ForeignKey(Door, on_delete=models.CASCADE)
    date_time = models.DateTimeField()

    def __str__(self):
        """Return the string representation of a log entry for readability in the admin site."""
        return f"User {self.user.username} entered door {self.door.id} at datetime {self.date_time}"
    
    def as_dict(self):
        """Return a dictionary representation of a log entry"""
        return {
            'uid': self.user.id,
            'door_id': self.door.id,
            'door_desc': self.door.descriptor,
            'accessed': self.date_time.strftime('%Y-%m-%d %H:%M')
        }