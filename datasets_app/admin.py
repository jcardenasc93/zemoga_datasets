from django.contrib import admin
from datasets_app.models import Namespace

# Register your models here.
app_models = [Namespace]
admin.site.register(app_models)
