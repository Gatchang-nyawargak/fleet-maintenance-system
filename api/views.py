from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
import logging

from maintenance.models import MaintenanceTask
from vehicles.models import Vehicle
from .serializers import MaintenanceTaskSerializer, VehicleSerializer

logger = logging.getLogger(__name__)

# Define a filter class for MaintenanceTask to allow filtering by related vehicle registration, task type, or status.
class MaintenanceTaskFilter(filters.FilterSet):
    registration_number = filters.CharFilter(
        field_name='vehicle__registration_number', lookup_expr='icontains'
    )
    task_type = filters.CharFilter(field_name='task_type', lookup_expr='icontains')
    status = filters.CharFilter(field_name='status', lookup_expr='icontains')

    class Meta:
        model = MaintenanceTask
        fields = ['vehicle__registration_number', 'task_type', 'status']

"""
MaintenanceTaskListView:
  - GET /tasks/ → Retrieve a list of all maintenance tasks.
  - POST /tasks/ → Create a new maintenance task.
"""
class MaintenanceTaskListView(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = MaintenanceTaskFilter  # Apply custom filtering

    def get(self, request):
        logger.info("Fetching all maintenance tasks")
        tasks = MaintenanceTask.objects.all()
        filtered_tasks = self.filterset_class(request.GET, queryset=tasks)
        serializer = MaintenanceTaskSerializer(filtered_tasks.qs, many=True)
        logger.info(f"{len(filtered_tasks.qs)} maintenance tasks retrieved.")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        logger.info("Creating a new maintenance task")
        serializer = MaintenanceTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Maintenance task created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Maintenance task creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
MaintenanceTaskDetailView:
  - GET /tasks/{id}/ → Retrieve details of a specific maintenance task.
  - POST /tasks/{id}/ → Update (full update) an existing maintenance task.
  - PATCH /tasks/{id}/ → Partially update an existing maintenance task.
  - DELETE /tasks/{id}/ → Remove a maintenance task.
"""
class MaintenanceTaskDetailView(APIView):
    def get(self, request, task_id):
        try:
            logger.info(f"Fetching maintenance task with ID: {task_id}")
            task = MaintenanceTask.objects.get(id=task_id)
            serializer = MaintenanceTaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MaintenanceTask.DoesNotExist:
            logger.error(f"Maintenance task with ID {task_id} not found")
            return Response({"error": "Maintenance task not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, task_id):
        """
        Allows a full update of the maintenance task via POST.
        """
        try:
            logger.info(f"Updating maintenance task with POST for ID: {task_id}")
            task = MaintenanceTask.objects.get(id=task_id)
            serializer = MaintenanceTaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Maintenance task with ID {task_id} updated successfully via POST")
                return Response(serializer.data, status=status.HTTP_200_OK)
            logger.error(f"Maintenance task update via POST failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MaintenanceTask.DoesNotExist:
            logger.error(f"Maintenance task with ID {task_id} not found for POST")
            return Response({"error": "Maintenance task not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, task_id):
        try:
            logger.info(f"Partially updating maintenance task with ID: {task_id}")
            task = MaintenanceTask.objects.get(id=task_id)
            serializer = MaintenanceTaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Maintenance task with ID {task_id} updated successfully via PATCH")
                return Response(serializer.data, status=status.HTTP_200_OK)
            logger.error(f"Maintenance task update failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MaintenanceTask.DoesNotExist:
            logger.error(f"Maintenance task with ID {task_id} not found")
            return Response({"error": "Maintenance task not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, task_id):
        try:
            logger.info(f"Deleting maintenance task with ID: {task_id}")
            task = MaintenanceTask.objects.get(id=task_id)
            task.delete()
            logger.info(f"Maintenance task with ID {task_id} deleted successfully")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except MaintenanceTask.DoesNotExist:
            logger.error(f"Maintenance task with ID {task_id} not found")
            return Response({"error": "Maintenance task not found"}, status=status.HTTP_404_NOT_FOUND)

"""
VehicleViewSet:
  - Provides full CRUD operations for vehicles.
"""
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['registration_number', 'make', 'model', 'year']
