from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from django.utils.timezone import now
import uuid

class BaseResource(resources.ModelResource):
    COMMON_FIELDS = (
        'id', 'created_by', 'updated_by', 'deleted_by', 'created_at', 'updated_at', 'is_deleted'
    )

    def before_import_row(self, row, **kwargs):
        user = kwargs.get('user')
        if user and user.is_authenticated and user.is_superuser:
            if 'id' not in row:
                row['id'] = str(uuid.uuid4())

            if 'created_by' not in row and user:
                row['created_by'] = user.id

            if 'updated_by' not in row and user:
                row['updated_by'] = user.id

            if 'is_deleted' not in row:
                row['is_deleted'] = False

            if 'is_deleted' in row and row['is_deleted'] == '1':
                row['deleted_by'] = user.id if user else None
                row['deleted_at'] = now()
        return row

