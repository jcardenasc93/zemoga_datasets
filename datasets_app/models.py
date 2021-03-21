from djongo import models


class AppBaseModel(models.Model):
    objects = models.DjongoManager()

    class Meta:
        abstract = True


class Namespace(AppBaseModel):
    """ Namespace model definition """
    _id = models.ObjectIdField()
    namespace_id = models.CharField(max_length=150, db_column='namespace_id')
    namespace_option_name = models.CharField(max_length=150,
                                             db_column='namespace_option_name')
    namespace_option_standard_name = models.CharField(
        max_length=150, db_column='namespace_option_standard_name')

    class Meta:
        db_table = 'namespace'


class DataPoint(AppBaseModel):
    """ Datapoint model definiton """
    _id = models.ObjectIdField()
    data_point_id = models.CharField(max_length=150, db_column='data_point_id')
    data_point_name = models.CharField(max_length=150,
                                       db_column='data_point_name')
    data_point_name_standard_name = models.CharField(
        max_length=150, db_column='data_point_standard_name')
    approved_abreviations = models.CharField(max_length=150,
                                             db_column='approved_abreviations')
    data_point_definition = models.CharField(max_length=250,
                                             db_column='data_point_definition')
    applicable_data_universes = models.CharField(
        max_length=50, db_column='applicable_data_universes')
    applicable_domicile = models.TextField(db_column='applicable_domicile')
    data_type = models.CharField(max_length=50, db_column='data_type')
    data_point_possible_values = models.CharField(
        max_length=150, db_column='data_point_possible_values')
    is_derived = models.CharField(max_length=50, db_column='is_derived')
    methodology_reference = models.CharField(max_length=150,
                                             db_column='methodology_reference')

    class Meta:
        db_table = 'datapoint'


class Column(AppBaseModel):
    """ Column model definition """
    _id = models.ObjectIdField()
    column_id = models.CharField(max_length=150, db_column='column_id')
    namespace_id = models.UUIDField(db_column='namespace_id')
    dataset_database_name = models.CharField(max_length=255,
                                             db_column='dataset_database_name')
    dataset_table_name = models.CharField(max_length=255,
                                          db_column='dataset_table_name')
    dataset_column_name = models.CharField(max_length=255,
                                           db_column='dataset_column_name')
    data_point_id = models.UUIDField(db_column='data_point_id')
    dataset_owner_name = models.CharField(max_length=150,
                                          db_column='dataset_owner_name')

    class Meta:
        db_table = 'column'


class DatasetFiles(models.Model):
    """ DatasetFile model definiton """
    namespaces_file = models.FileField()
    datapoints_file = models.FileField()
    columns_file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Dataset(AppBaseModel):
    """ Datasets model definition """
    _id = models.ObjectIdField()
    name = models.CharField(max_length=50, db_column='name')
    datasets = models.EmbeddedField(model_container=DatasetFiles)
