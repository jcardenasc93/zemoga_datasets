""" Datasets urls routing """
from django.urls import path
from datasets_app.views import datasets_view, fetch_datasets, generate_json_file

urlpatterns = [
    path(r'', datasets_view, name='datasets'),
    path(r'fetch', fetch_datasets, name='fetch_data'),
    path(r'report', generate_json_file, name='json_report')
]
