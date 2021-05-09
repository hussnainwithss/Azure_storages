from django.db import models

class AzureAccessKey(models.Model):
    name=models.CharField(max_length=255)
    connection_string=models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DownloadPath(models.Model):
    path = models.CharField(max_length=1000)

    def __str__(self):
        return self.path