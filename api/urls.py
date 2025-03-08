from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import VehicleViewSet, MaintenanceTaskListView, MaintenanceTaskDetailView

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet)

urlpatterns = [
    path('tasks/', MaintenanceTaskListView.as_view(), name='maintenance-task-list'),
    path('tasks/<int:task_id>/', MaintenanceTaskDetailView.as_view(), name='maintenance-task-detail'),
    path('', include(router.urls)),
]

