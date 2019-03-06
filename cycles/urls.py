from django.conf.urls import url, defaults
from django.urls import path, include
from . import views

app_name = "cycles"

urlpatterns = [
    path('', views.cyclelist, name='cyclelist'),
    url(r'^login$', views.login_user, name='login'),
    url(r'^logout$', views.user_logout, name='logout'),
    url(r'^register$', views.register, name='register'),
    path('deleteCycle/<int:cycle_id>', views.deleteCycle, name='deleteCycle'),
    path('deleteTenant/<int:tenant_id>', views.deleteTenant, name='deleteTenant'),
    path('editTenant/<int:tenant_id>', views.editTenant, name='editTenant'),
    path('editTenantForm/<int:tenant_id>', views.editTenantForm, name='editTenantForm'),
    path("tenants/", views.tenantlist, name="tenantlist"),
]