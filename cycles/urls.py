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
    path('cycleDetail/<int:cycle_id>', views.cycleDetail, name='cycleDetail'),
    path('deleteTenant/<int:tenant_id>', views.deleteTenant, name='deleteTenant'),
    path('editTenant/<int:tenant_id>', views.editTenant, name='editTenant'),
    path('editTenantForm/<int:tenant_id>', views.editTenantForm, name='editTenantForm'),
    path('addTenantForm/', views.addTenantForm, name='addTenantForm'),
    path('addTenant/', views.addTenant, name='addTenant'),
    path("tenants/", views.tenantlist, name="tenantlist"),
    path('deleteRecurring/<int:recurring_id>', views.deleteRecurring, name='deleteRecurring'),
    path('editRecurring/<int:recurring_id>', views.editRecurring, name='editRecurring'),
    path('editRecurringForm/<int:recurring_id>', views.editRecurringForm, name='editRecurringForm'),
    path('addRecurringForm/', views.addRecurringForm, name='addRecurringForm'),
    path('addRecurring/', views.addRecurring, name='addRecurring'),
    path("recurring/", views.recurringlist, name="recurringlist"),
    path('deleteBill/<int:bill_id>', views.deleteBill, name='deleteBill'),
    path('editBill/<int:bill_id>', views.editBill, name='editBill'),
    path('editBillForm/<int:bill_id>', views.editBillForm, name='editBillForm'),
    path('addRecurringForm/<int:cycle_id>', views.addRecurringForm, name='addRecurringForm'),
    path('addRecurring/<int:cycle_id>', views.addRecurring, name='addRecurring'),
    path('addOneTimeForm/<int:cycle_id>', views.addOneTimeForm, name='addOneTimeForm'),
    path('addOneTime/<int:cycle_id>', views.addOneTime, name='addOneTime'),
    path("newCycleForm/", views.newCycleForm, name="newCycleForm"),
    path("newCycle/", views.newCycle, name="newCycle"),
]