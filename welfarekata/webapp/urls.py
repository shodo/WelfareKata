from rest_framework.routers import DefaultRouter

from welfarekata.webapp.views.api.employee_view_set import EmployeeViewSet

app_name = 'webapp'

employees_router_v1 = DefaultRouter()
employees_router_v1.register('employees',
                             EmployeeViewSet,
                             basename='employees')

urlpatterns = []
