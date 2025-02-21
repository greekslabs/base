from django.contrib import admin
from django.contrib.admin import AdminSite
from accounts.models import User 

class BaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'created_at', 'updated_at')
    list_filter = ('created_by', 'is_deleted')
    search_fields = ('created_by__username',)  # Assuming User has a 'username' field
    readonly_fields = ('id', 'created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
    # Only show records created by the logged-in user
        return queryset.filter(is_deleted=False)



class GreekslabAdminSite(AdminSite):
    """
    Custom admin site for Greekslab.
    """
    site_header = "Greekslab Admin"
    site_title = "Greekslab Admin Portal"
    index_title = "Welcome to the Greekslab Admin Panel"


    def has_permission(self, request):
        """
        Allow only users with 'Greekslab' role to access the admin panel.
        """
        return request.user.is_active and request.user.is_staff and request.user.role == User.GREEKSLAB



# Instantiate the custom admin site
greekslab_admin_site = GreekslabAdminSite(name='greekslab_admin')