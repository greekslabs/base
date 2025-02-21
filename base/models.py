from django.db import models
import uuid

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(
        "accounts.User", blank=True, null=True, related_name="created_by_%(class)s_objects", on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(
        "accounts.User", blank=True, null=True, related_name="updated_by_%(class)s_objects", on_delete=models.CASCADE
    )
    deleted_by = models.ForeignKey(
        "accounts.User", blank=True, null=True, related_name="deleted_by_%(class)s_objects", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
