from django.db import models

# Create your models here.

class NodePin(models.Model):
	nodepin = models.CharField(max_length=200, null=False, blank=False, unique=True)

class GenSetData(models.Model):
	nodepin = models.CharField(max_length = 200)
	date = models.DateTimeField(blank=True)
	avg_voltage = models.IntegerField(default=0)
	avg_current = models.IntegerField(default=0)
	avg_load = models.IntegerField(default=0)
	status_tag = models.CharField(max_length = 200, blank=True)
