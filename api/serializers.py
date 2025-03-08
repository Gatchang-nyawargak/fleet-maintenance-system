from rest_framework import serializers
from maintenance.models import MaintenanceTask
from vehicles.models import Vehicle

class MaintenanceTaskSerializer(serializers.ModelSerializer):
    vehicle_registration = serializers.CharField(source='vehicle.registration_number', read_only=True)
    
    class Meta:
        model = MaintenanceTask
        fields = [
            'id', 'vehicle', 'vehicle_registration', 'task_type', 
            'description', 'date_performed', 'technician', 
            'status', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_vehicle(self, value):
        """
        Check that the vehicle exists.
        """
        if not Vehicle.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Vehicle does not exist")
        return value

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'