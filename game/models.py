from django.conf import settings
from django.db import models

class GameHistory(models.Model):
    LEVEL_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # <- use this instead of User
        on_delete=models.CASCADE,
        related_name="histories"  # optional, but useful for reverse lookups
    )
    score = models.IntegerField(default=0)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    time_taken = models.IntegerField(help_text="Time taken in seconds", default=0)
    date_played = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.level} - {self.score}"
