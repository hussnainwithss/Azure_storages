from django.contrib import admin
from .models import AzureAccessKey,DownloadPath
# Register your models here.

admin.site.register(AzureAccessKey)
admin.site.register(DownloadPath)