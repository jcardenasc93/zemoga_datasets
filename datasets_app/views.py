from django.shortcuts import render
from bson.json_util import dumps

# Models
from datasets_app.models import Dataset
# Forms
from datasets_app.forms import DatasetForm

def datasets_view(request):
    """ This view lists and allows datasets creation """
    DATASETS_TEMPLATE = 'datasets_app/datasets.html'
    # Define queryset to retrieve all existing datasets
    queryset = Dataset.objects.mongo_find()
    form = DatasetForm()

    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            # If form validation is success then save create dataset
            form.save()
    context = {'datasets': queryset, 'form': form}
    return render(request, DATASETS_TEMPLATE, context)

