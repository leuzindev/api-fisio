from django.db import models

# Create your models here.

class Professional(models.Model):
	name = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	password = models.CharField(max_length=255)

	updated_At = models.DateField(auto_now=True, blank=True)

	def __str__(self):
			return self.name