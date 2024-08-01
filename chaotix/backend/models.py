from django.db import models

class GeneratedImage(models.Model):
    url = models.URLField()
    metadata = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.url