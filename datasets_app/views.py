from django.shortcuts import render
from django.http import HttpResponse

# Models
from datasets_app.models import Dataset, Namespace, Column, DataPoint
# Forms
from datasets_app.forms import DatasetForm

# utils
from datasets_app.utils.clean_data import CleanDataset
from datasets_app.utils.fetch_related_data import ContextBuilder, ContextMemory
from datasets_app.utils.json_builder import JSONFileBuilder
from datasets_app.utils.csv_builder import CSVFileBuilder

# Initialize context memory
context_memory = ContextMemory()


def datasets_view(request):
    """ This view lists and allows datasets creation """
    DATASETS_TEMPLATE = 'datasets_app/datasets.html'
    # Define queryset to retrieve all existing datasets
    queryset = Dataset.objects.mongo_find()
    form = DatasetForm()
    context_memory.clear_context()

    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            # If form validation is success then save create dataset
            dataset = form.save()
            namespace_file = dataset.namespaces_file
            columns_file = dataset.columns_file
            datapoints_file = dataset.datapoints_file

            # Creates dataframes
            dataset_data = CleanDataset(dataset.dataset_id, namespace_file,
                                        columns_file, datapoints_file)
            # Upload dataframes to mongo
            dataset_data.load_data()

            # Report anomalies
            CSVFileBuilder.write_file(dataset_data.retrieve_found_anomalies())
            # Get csv file
            csv_file, mime_type = CSVFileBuilder.download_file()

            # Includes csv file in HTTP response
            response = HttpResponse(csv_file, content_type=mime_type)
            response[
                'Content-Disposition'] = f"attachment; filename=anomalies_report.csv"
            return response

    context = {'datasets': queryset, 'form': form}
    return render(request, DATASETS_TEMPLATE, context)


def fetch_datasets(request):
    """ This view process the user selection across
    namespaces, databases, tables, columns and datapoints
    to retrieve the desired datapoint info
    """
    FETCH_TEMPLATE = 'datasets_app/fetch_data.html'
    selection_history = []
    if request.method == 'POST':
        # Retrieves context
        context = ContextBuilder().build_context(request,
                                                 context_memory.context)
        # Updates context memory
        context_memory.context = context
        return render(request, FETCH_TEMPLATE, context)
    context = ContextBuilder().build_context(request, context_memory.context)
    return render(request, FETCH_TEMPLATE, context)


def generate_json_file(request):
    """ This view generate the JSON file
    accordign with the matching datapoints
    """
    if request.method == "POST":
        column_name = request.POST.get('column_name')
        file_name = request.POST.get('file_name')
        dataset_id = context_memory.context.get('dataset_id')
        datapoints_ids = set(
            Column.objects.filter(dataset_column_name=column_name,
                                  dataset_id=dataset_id).values_list(
                                      'data_point_id',
                                      flat=True)) if column_name else None
        print(datapoints_ids, dataset_id)
        datapoints = DataPoint.objects.filter(data_point_id__in=datapoints_ids,
                                              dataset_id=dataset_id)

        # Initialize JSONBuilder
        json_builder = JSONFileBuilder(context_memory.context)
        json_builder.fill_data_points(datapoints)
        json_builder.build_structure()
        json_builder.create_json_file(file_name)
        json_file, mime_type = json_builder.download_file(file_name)

        # Includes file in the HTTP reponse
        response = HttpResponse(json_file, content_type=mime_type)
        response[
            'Content-Disposition'] = f"attachment; filename={file_name}.json"
        return response
