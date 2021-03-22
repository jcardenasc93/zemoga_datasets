""" Fetch related data module """

from datasets_app.models import Dataset, Namespace, Column, DataPoint


class ContextMemory:

    def __init__(self):
        self._context = {}

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, new_context):
        """ This method adds new keys to context and updates those
        that its value is None"""
        for key in new_context.keys():
            if key not in self.context:
                self._context[key] = new_context.get(key)
            else:
                if not self._context.get(key) and new_context.get(key):
                    self._context[key] = new_context.get(key)

    def clear_context(self):
        """ Clears context """
        self._context = {}


class ContextBuilder:
    """ This class is used any time a user makes a selection related
    to Namespace, Column, or DataPoint models
    """

    @classmethod
    def build_context(cls, request, context_memory):
        """ method to build context according to received request
        Args:
            request (RequestObject): The view request
        Returns:
            context (dict): The context to render in template"""
        # Get user selections values
        dataset_id = request.POST.get('dataset_id')
        namespace_id = request.POST.get('namespace_id')
        database_name = request.POST.get('database_name')
        table_name = request.POST.get('table_name')
        column_name = request.POST.get('column_name')

        # Context memory aditional attributes
        namespace = None
        owner_name = None
        dataset_databases = None
        dataset_datapoints = None

        # Query options based on user selections
        if not dataset_id:
            # Retrieves dataset id from Context memory
            dataset_id = context_memory['dataset_id']
        dataset_namespaces = Namespace.objects.filter(
            dataset_id=dataset_id) if dataset_id else None
        if namespace_id:
            namespace = Namespace.objects.get(namespace_id=namespace_id,
                                              dataset_id=dataset_id)
            column_query = Column.objects.filter(namespace_id=namespace_id,
                                                 dataset_id=dataset_id)
            owner_name = column_query[0].dataset_owner_name if len(
                column_query) else None
            dataset_databases = set(
                column_query.values_list('dataset_database_name', flat=True))
        if not dataset_id:
            dataset_id = context_memory['dataset_id']
        dataset_tables = set(
            Column.objects.filter(dataset_database_name=database_name,
                                  dataset_id=dataset_id).values_list(
                                      'dataset_table_name',
                                      flat=True)) if database_name else None
        dataset_columns = set(
            Column.objects.filter(dataset_table_name=table_name,
                                  dataset_id=dataset_id).values_list(
                                      'dataset_column_name',
                                      flat=True)) if table_name else None
        if column_name:
            dataset_datapoints = set(
                Column.objects.filter(dataset_column_name=column_name,
                                      dataset_id=dataset_id).values_list(
                                          'data_point_id', flat=True))
            dataset_datapoints = set(
                DataPoint.objects.filter(data_point_id__in=dataset_datapoints,
                                         dataset_id=dataset_id))

        context = {
            # Options
            "namespaces": dataset_namespaces,
            "databases": dataset_databases,
            "tables": dataset_tables,
            "columns": dataset_columns,

            # User selection
            "dataset_id": dataset_id,
            "namespace": namespace,
            "owner_name": owner_name,
            "database_name": database_name,
            "table_name": table_name,
            "column_name": column_name,

            # Matching datapoints
            "datapoints": dataset_datapoints
        }
        return context
