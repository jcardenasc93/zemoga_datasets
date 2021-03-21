from django.contrib import admin
from datasets_app.models import Namespace, Dataset

# Register your models here.
app_models = [Namespace, Dataset]
admin.site.register(app_models)
