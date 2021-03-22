from django.shortcuts import render

# Models
from datasets_app.models import Dataset, Namespace, Column, DataPoint
# Forms
from datasets_app.forms import DatasetForm

# utils
from datasets_app.utils.clean_data import CleanDataset

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
            dataset = form.save()
            namespace_file = dataset.namespaces_file
            columns_file = dataset.columns_file
            datapoints_file = dataset.datapoints_file

            # Creates dataframes
            dataset_data = CleanDataset(dataset.pk, namespace_file, columns_file, datapoints_file)
            # Upload dataframes to mongo
            dataset_data.load_data()

    context = {'datasets': queryset, 'form': form}
    return render(request, DATASETS_TEMPLATE, context)

def fetch_datasets(request):
    """ This view process the files content and match
    the info of the selected dataset
    """
    if request.method == 'POST':
        # Retrieves the dataset files locations from dataset info
        dataset = Dataset.objects.get(dataset_id=request.POST.get('dataset_id'))

