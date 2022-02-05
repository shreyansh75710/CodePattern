from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.codeSnippet)
admin.site.register(models.comment)
admin.site.register(models.theoryNote)