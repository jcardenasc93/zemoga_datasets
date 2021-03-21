""" Datasets urls routing """
from django.urls import path
from datasets_app.views import datasets_view

urlpatterns = [
    path(r'', datasets_view, name='datasets')
]
